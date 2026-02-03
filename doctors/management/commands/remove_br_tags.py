from django.core.management.base import BaseCommand
from doctors.models import Doctor
import re


class Command(BaseCommand):
    help = 'Remove all <br> tags from database fields'

    def handle(self, *args, **options):
        doctors = Doctor.objects.all()
        updated_count = 0
        
        for doctor in doctors:
            updated = False
            
            # Remove <br> from name
            if '<br>' in doctor.name or '<br/>' in doctor.name or '<BR>' in doctor.name:
                doctor.name = re.sub(r'<br\s*/?>', ' ', doctor.name, flags=re.IGNORECASE)
                doctor.name = re.sub(r'\s+', ' ', doctor.name).strip()
                updated = True
            
            # Remove <br> from qualification
            if doctor.qualification and ('<br>' in doctor.qualification or '<br/>' in doctor.qualification or '<BR>' in doctor.qualification):
                doctor.qualification = re.sub(r'<br\s*/?>', ' ', doctor.qualification, flags=re.IGNORECASE)
                doctor.qualification = re.sub(r'\s+', ' ', doctor.qualification).strip()
                updated = True
            
            # Remove <br> from specialty
            if doctor.specialty and ('<br>' in doctor.specialty or '<br/>' in doctor.specialty or '<BR>' in doctor.specialty):
                doctor.specialty = re.sub(r'<br\s*/?>', ' ', doctor.specialty, flags=re.IGNORECASE)
                doctor.specialty = re.sub(r'\s+', ' ', doctor.specialty).strip()
                updated = True
            
            # Remove <br> from schedule
            if doctor.schedule and ('<br>' in doctor.schedule or '<br/>' in doctor.schedule or '<BR>' in doctor.schedule):
                doctor.schedule = re.sub(r'<br\s*/?>', '\n', doctor.schedule, flags=re.IGNORECASE)
                updated = True
            
            # Remove <br> from hospital
            if doctor.hospital and ('<br>' in doctor.hospital or '<br/>' in doctor.hospital or '<BR>' in doctor.hospital):
                doctor.hospital = re.sub(r'<br\s*/?>', ' ', doctor.hospital, flags=re.IGNORECASE)
                doctor.hospital = re.sub(r'\s+', ' ', doctor.hospital).strip()
                updated = True
            
            # Remove <br> from hospital_address
            if doctor.hospital_address and ('<br>' in doctor.hospital_address or '<br/>' in doctor.hospital_address or '<BR>' in doctor.hospital_address):
                doctor.hospital_address = re.sub(r'<br\s*/?>', ' ', doctor.hospital_address, flags=re.IGNORECASE)
                doctor.hospital_address = re.sub(r'\s+', ' ', doctor.hospital_address).strip()
                updated = True
            
            # Remove <br> from contact (keep as single line)
            if doctor.contact and ('<br>' in doctor.contact or '<br/>' in doctor.contact or '<BR>' in doctor.contact):
                doctor.contact = re.sub(r'<br\s*/?>', ', ', doctor.contact, flags=re.IGNORECASE)
                doctor.contact = re.sub(r'\s*,\s*', ', ', doctor.contact)
                doctor.contact = re.sub(r',\s*,', ',', doctor.contact).strip()
                updated = True
            
            if updated:
                doctor.save()
                updated_count += 1
                self.stdout.write(f'Updated: {doctor.name}')
        
        self.stdout.write(self.style.SUCCESS(f'\nTotal doctors updated: {updated_count}'))
