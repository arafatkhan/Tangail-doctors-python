# -*- coding: utf-8 -*-
"""
Management command to split hospital field into name and address
Hospital data usually has name and location separated by <br> tag
"""
from django.core.management.base import BaseCommand
from doctors.models import Doctor
import re


class Command(BaseCommand):
    help = 'Split hospital field into name and address'

    def handle(self, *args, **kwargs):
        doctors = Doctor.objects.all()
        updated_count = 0
        
        for doctor in doctors:
            if doctor.hospital:
                # Split by <br> tag
                parts = re.split(r'<br\s*/?>', doctor.hospital, flags=re.IGNORECASE)
                
                if len(parts) > 1:
                    # First part is hospital name, rest is address
                    doctor.hospital = parts[0].strip()
                    doctor.hospital_address = ' '.join(parts[1:]).strip()
                    doctor.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Updated: {doctor.name} - {doctor.hospital}')
                    )
                else:
                    # No <br> tag, keep everything in hospital name
                    doctor.hospital = doctor.hospital.strip()
                    doctor.hospital_address = ''
                    doctor.save()
                    updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'\nTotal doctors updated: {updated_count}')
        )
