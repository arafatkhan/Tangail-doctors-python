# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from doctors.models import Doctor, Category, CategoryKeyword


class Command(BaseCommand):
    help = 'Migrate hardcoded CATEGORY_MAPPING to database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting category migration...'))
        
        # Icon mapping for categories
        ICON_MAPPING = {
            'প্রসূতি ও স্ত্রীরোগ বিশেষজ্ঞ': 'fa-baby',
            'সার্জারি বিশেষজ্ঞ': 'fa-scalpel',
            'শিশু বিশেষজ্ঞ': 'fa-child',
            'হৃদরোগ বিশেষজ্ঞ': 'fa-heart-pulse',
            'চর্মরোগ বিশেষজ্ঞ': 'fa-hand-dots',
            'মেডিসিন বিশেষজ্ঞ': 'fa-user-doctor',
            'চক্ষু বিশেষজ্ঞ': 'fa-eye',
            'দাঁতের চিকিৎসক': 'fa-tooth',
            'হাড় ও জয়েন্ট বিশেষজ্ঞ': 'fa-bone',
            'নাক-কান-গলা বিশেষজ্ঞ': 'fa-ear-listen',
            'কিডনী রোগ বিশেষজ্ঞ': 'fa-kidney',
            'মানসিক রোগ বিশেষজ্ঞ': 'fa-brain',
            'নিউরো বিশেষজ্ঞ': 'fa-head-side-virus',
            'আলট্রাসনোগ্রাম বিশেষজ্ঞ': 'fa-wave-square',
            'ক্যান্সার/অনকোলজি বিশেষজ্ঞ': 'fa-ribbon',
            'প্লাস্টিক সার্জারি': 'fa-hand-sparkles',
            'রক্ত রোগ বিশেষজ্ঞ': 'fa-droplet',
            'পুষ্টি বিশেষজ্ঞ': 'fa-apple-whole',
            'এন্ডোক্রাইনোলজি/ডায়াবেটিস': 'fa-syringe',
            'অন্যান্য বিশেষজ্ঞ': 'fa-stethoscope',
        }
        
        # Color mapping for categories
        COLOR_MAPPING = {
            'প্রসূতি ও স্ত্রীরোগ বিশেষজ্ঞ': 'danger',
            'সার্জারি বিশেষজ্ঞ': 'warning',
            'শিশু বিশেষজ্ঞ': 'info',
            'হৃদরোগ বিশেষজ্ঞ': 'danger',
            'চর্মরোগ বিশেষজ্ঞ': 'secondary',
            'মেডিসিন বিশেষজ্ঞ': 'primary',
            'চক্ষু বিশেষজ্ঞ': 'success',
            'দাঁতের চিকিৎসক': 'info',
            'হাড় ও জয়েন্ট বিশেষজ্ঞ': 'warning',
            'নাক-কান-গলা বিশেষজ্ঞ': 'primary',
            'কিডনী রোগ বিশেষজ্ঞ': 'danger',
            'মানসিক রোগ বিশেষজ্ঞ': 'secondary',
            'নিউরো বিশেষজ্ঞ': 'warning',
            'আলট্রাসনোগ্রাম বিশেষজ্ঞ': 'info',
            'ক্যান্সার/অনকোলজি বিশেষজ্ঞ': 'danger',
            'প্লাস্টিক সার্জারি': 'success',
            'রক্ত রোগ বিশেষজ্ঞ': 'danger',
            'পুষ্টি বিশেষজ্ঞ': 'success',
            'এন্ডোক্রাইনোলজি/ডায়াবেটিস': 'warning',
            'অন্যান্য বিশেষজ্ঞ': 'secondary',
        }
        
        # Create categories from CATEGORY_MAPPING
        category_count = 0
        keyword_count = 0
        
        for order, (category_name, keywords) in enumerate(Doctor.CATEGORY_MAPPING.items(), start=1):
            # Generate unique slug
            base_slug = slugify(category_name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exclude(name=category_name).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            
            category, created = Category.objects.update_or_create(
                name=category_name,
                defaults={
                    'slug': slug,
                    'icon': ICON_MAPPING.get(category_name, 'fa-stethoscope'),
                    'color': COLOR_MAPPING.get(category_name, 'primary'),
                    'order': order,
                    'is_active': True,
                }
            )
            
            if created:
                category_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✅ Created category: {category_name}'))
            else:
                self.stdout.write(f'  ℹ️  Category already exists: {category_name}')
            
            # Add keywords for this category
            for keyword in keywords:
                keyword_obj, created = CategoryKeyword.objects.get_or_create(
                    category=category,
                    keyword=keyword,
                    defaults={'is_active': True}
                )
                if created:
                    keyword_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Created {category_count} new categories'))
        self.stdout.write(self.style.SUCCESS(f'✅ Created {keyword_count} new keywords'))
        
        # Auto-assign categories to all doctors
        self.stdout.write('\nAssigning categories to doctors...')
        doctor_count = 0
        for doctor in Doctor.objects.all():
            doctor.auto_assign_categories()
            doctor_count += 1
            if doctor_count % 50 == 0:
                self.stdout.write(f'  Processed {doctor_count} doctors...')
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Assigned categories to {doctor_count} doctors'))
        self.stdout.write(self.style.SUCCESS('\n🎉 Migration completed successfully!'))
