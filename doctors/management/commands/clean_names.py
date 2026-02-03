from django.core.management.base import BaseCommand
from doctors.models import Doctor
import re


class Command(BaseCommand):
    help = 'Clean <br> tags from doctor names'

    def handle(self, *args, **options):
        doctors = Doctor.objects.all()
        updated_count = 0
        
        self.stdout.write('🧹 Cleaning doctor names...\n')
        
        for doctor in doctors:
            original_name = doctor.name
            
            # Remove <br> tags (case insensitive)
            cleaned_name = re.sub(r'<br\s*/?>', ' ', doctor.name, flags=re.IGNORECASE)
            
            # Remove multiple spaces
            cleaned_name = re.sub(r'\s+', ' ', cleaned_name)
            
            # Trim whitespace
            cleaned_name = cleaned_name.strip()
            
            if cleaned_name != original_name:
                doctor.name = cleaned_name
                doctor.save()
                updated_count += 1
                self.stdout.write(
                    f'✅ Updated: "{original_name}" → "{cleaned_name}"'
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Cleanup complete! Updated {updated_count} doctors.'
            )
        )
