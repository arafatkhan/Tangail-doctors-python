# -*- coding: utf-8 -*-
import json
import os
from django.core.management.base import BaseCommand
from doctors.models import Doctor


class Command(BaseCommand):
    help = 'Import doctors from data.json'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before import',
        )
    
    def handle(self, *args, **options):
        # Find data.json
        json_path = os.path.join(os.getcwd(), 'data.json')
        
        if not os.path.exists(json_path):
            self.stdout.write(
                self.style.ERROR(f'❌ data.json not found at {json_path}')
            )
            return
        
        # Load JSON data
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                doctors_data = json.load(f)
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error reading JSON: {e}')
            )
            return
        
        # Clear existing data if requested
        if options['clear']:
            Doctor.objects.all().delete()
            self.stdout.write(
                self.style.WARNING('⚠️  Cleared existing doctor data')
            )
        
        # Import data
        success_count = 0
        error_count = 0
        
        for data in doctors_data:
            try:
                doctor, created = Doctor.objects.update_or_create(
                    name=data.get('name', '').strip(),
                    defaults={
                        'qualification': data.get('qualification', ''),
                        'specialty': data.get('specialty', ''),
                        'schedule': data.get('schedule', ''),
                        'hospital': data.get('hospital', ''),
                        'contact': data.get('contact', ''),
                        'is_active': True,
                    }
                )
                success_count += 1
                
                if created:
                    self.stdout.write(f'✅ Created: {doctor.name}')
                else:
                    self.stdout.write(f'🔄 Updated: {doctor.name}')
                    
            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(
                        f'❌ Error importing {data.get("name", "Unknown")}: {e}'
                    )
                )
        
        # Summary
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Import complete!'
                f'\n   Success: {success_count}'
                f'\n   Errors: {error_count}'
                f'\n   Total in DB: {Doctor.objects.count()}'
            )
        )
