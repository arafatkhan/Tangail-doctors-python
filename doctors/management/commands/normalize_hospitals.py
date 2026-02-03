# -*- coding: utf-8 -*-
"""
Management command to normalize hospital names
Remove line breaks, extra spaces, and standardize names
"""
from django.core.management.base import BaseCommand
from doctors.models import Doctor
import re


class Command(BaseCommand):
    help = 'Normalize hospital names by removing line breaks and extra spaces'

    def handle(self, *args, **kwargs):
        doctors = Doctor.objects.all()
        updated_count = 0
        
        for doctor in doctors:
            if doctor.hospital:
                # Remove <br> tags and line breaks
                original = doctor.hospital
                normalized = re.sub(r'<br\s*/?>', ' ', doctor.hospital, flags=re.IGNORECASE)
                normalized = re.sub(r'\s+', ' ', normalized)  # Replace multiple spaces with single space
                normalized = normalized.strip()
                
                if normalized != original:
                    doctor.hospital = normalized
                    doctor.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Updated: {original} → {normalized}')
                    )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nTotal hospitals normalized: {updated_count}')
        )
