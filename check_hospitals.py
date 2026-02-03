# -*- coding: utf-8 -*-
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from doctors.models import Doctor

# Find all hospitals with "আয়শা"
hospitals = Doctor.objects.filter(hospital__icontains='আয়শা').values('hospital').distinct()
print("Hospitals with 'আয়শা':")
for h in hospitals:
    count = Doctor.objects.filter(hospital=h['hospital']).count()
    print(f"  - {h['hospital']} ({count} doctors)")

# Fix the hospital names
Doctor.objects.filter(hospital='আয়শা খানম মেমোরিয়াল হাসপাতাল').update(hospital='আয়শা খানম মেমোরিয়াল হাসপাতাল')

print("\nAfter fix:")
hospitals = Doctor.objects.filter(hospital__icontains='আয়শা').values('hospital').distinct()
for h in hospitals:
    count = Doctor.objects.filter(hospital=h['hospital']).count()
    print(f"  - {h['hospital']} ({count} doctors)")
