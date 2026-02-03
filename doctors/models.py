# -*- coding: utf-8 -*-
from django.db import models
from django.utils.html import strip_tags
from django.utils.text import slugify
import re


class Category(models.Model):
    """ডাক্তারের ক্যাটেগরি"""
    name = models.CharField('নাম', max_length=100, unique=True)
    name_english = models.CharField('English Name', max_length=100, blank=True)
    slug = models.SlugField('স্লাগ', unique=True, max_length=150)
    description = models.TextField('বিবরণ', blank=True)
    icon = models.CharField('আইকন', max_length=50, default='fa-stethoscope', help_text='Font Awesome class (e.g., fa-heart)')
    color = models.CharField('রং', max_length=20, default='primary', help_text='Bootstrap color class')
    order = models.IntegerField('ক্রম', default=0, help_text='Display order (lower number = higher priority)')
    is_active = models.BooleanField('সক্রিয়', default=True)
    created_at = models.DateTimeField('তৈরি হয়েছে', auto_now_add=True)
    updated_at = models.DateTimeField('আপডেট হয়েছে', auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'ক্যাটেগরি'
        verbose_name_plural = 'ক্যাটেগরিসমূহ'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_doctor_count(self):
        """এই ক্যাটেগরিতে কতজন সক্রিয় ডাক্তার আছে"""
        return self.doctors.filter(is_active=True).count()


class CategoryKeyword(models.Model):
    """ক্যাটেগরি সনাক্তকরণের জন্য কীওয়ার্ড"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='keywords', verbose_name='ক্যাটেগরি')
    keyword = models.CharField('কীওয়ার্ড', max_length=100)
    is_active = models.BooleanField('সক্রিয়', default=True)
    
    class Meta:
        unique_together = ['category', 'keyword']
        verbose_name = 'ক্যাটেগরি কীওয়ার্ড'
        verbose_name_plural = 'ক্যাটেগরি কীওয়ার্ডসমূহ'
        ordering = ['category', 'keyword']
    
    def __str__(self):
        return f'{self.category.name} - {self.keyword}'


class Doctor(models.Model):
    """Doctor model for storing doctor information"""
    
    # Category mapping - class attribute
    CATEGORY_MAPPING = {
        'প্রসূতি ও স্ত্রীরোগ বিশেষজ্ঞ': [
            'প্রসূতি', 'স্ত্রী', 'গাইনী', 'গাইনি', 'অবস', 'গাইনোলজি'
        ],
        'সার্জারি বিশেষজ্ঞ': [
            'সার্জন', 'সার্জারি', 'শল্য', 'অপারেশন', 'ল্যাপারোস্কপিক'
        ],
        'শিশু বিশেষজ্ঞ': [
            'শিশু', 'নবজাতক', 'পেডিয়াট্রিক', 'কিশোর'
        ],
        'হৃদরোগ বিশেষজ্ঞ': [
            'হৃদরোগ', 'হার্ট', 'কার্ডিও', 'বাতজ্বর', 'হৃদ'
        ],
        'চর্মরোগ বিশেষজ্ঞ': [
            'চর্ম', 'ত্বক', 'যৌন', 'এলার্জি', 'স্কিন'
        ],
        'মেডিসিন বিশেষজ্ঞ': [
            'মেডিসিন', 'চিকিৎসক', 'ডায়াবেটিস', 'অভ্যন্তরীণ', 'বক্ষব্যাধি'
        ],
        'চক্ষু বিশেষজ্ঞ': [
            'চক্ষু', 'চোখ', 'অপথালমো', 'কেটারেক্ট', 'ছানি'
        ],
        'দাঁতের চিকিৎসক': [
            'দাঁত', 'ডেন্টাল', 'দন্ত', 'মুখ'
        ],
        'হাড় ও জয়েন্ট বিশেষজ্ঞ': [
            'হাড়', 'অর্থো', 'জয়েন্ট', 'ফিজিও', 'বাত', 'ব্যথা', 'পঙ্গু'
        ],
        'নাক-কান-গলা বিশেষজ্ঞ': [
            'নাক', 'কান', 'গলা', 'ইএনটি', 'ই এন টি', 'হেড নেক'
        ],
        'কিডনী রোগ বিশেষজ্ঞ': [
            'কিডনী', 'বৃক্ক', 'ডায়ালাইসিস', 'নেফ্রো', 'মূত্র'
        ],
        'মানসিক রোগ বিশেষজ্ঞ': [
            'মানসিক', 'সাইকিয়াট্রি', 'মনোরোগ'
        ],
        'নিউরো বিশেষজ্ঞ': [
            'নিউরো', 'স্নায়ু', 'মস্তিষ্ক', 'ব্রেইন'
        ],
        'আল্ট্রাসনোগ্রাম বিশেষজ্ঞ': [
            'আল্ট্রা', 'সনো', 'রেডিও', 'ইমেজিং'
        ],
    }
    
    name = models.CharField(
        max_length=200, 
        verbose_name='নাম',
        help_text='ডাক্তারের পূর্ণ নাম'
    )
    qualification = models.TextField(
        verbose_name='যোগ্যতা',
        help_text='শিক্ষাগত যোগ্যতা (HTML tags allowed)'
    )
    specialty = models.CharField(
        max_length=200, 
        verbose_name='বিশেষত্ব',
        help_text='বিশেষজ্ঞতার ক্ষেত্র'
    )
    schedule = models.TextField(
        verbose_name='সময়সূচী',
        help_text='চেম্বার সময়সূচী (HTML tags allowed)'
    )
    hospital = models.CharField(
        max_length=200, 
        verbose_name='হাসপাতাল',
        help_text='হাসপাতাল/ক্লিনিকের নাম'
    )
    hospital_address = models.TextField(
        blank=True,
        null=True,
        verbose_name='হাসপাতাল ঠিকানা',
        help_text='হাসপাতাল/ক্লিনিকের ঠিকানা (Optional)'
    )
    contact = models.CharField(
        max_length=200, 
        verbose_name='যোগাযোগ',
        help_text='ফোন নম্বর'
    )
    
    # Category relationships
    categories = models.ManyToManyField(
        Category, 
        related_name='doctors',
        blank=True,
        verbose_name='ক্যাটেগরিসমূহ',
        help_text='এই ডাক্তার যে সব ক্যাটেগরিতে আছেন'
    )
    primary_category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='primary_doctors',
        verbose_name='প্রধান ক্যাটেগরি',
        help_text='মূল বিশেষত্ব ক্যাটেগরি'
    )
    
    # Auto-generated fields
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='তৈরির সময়'
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name='সর্বশেষ আপডেট'
    )
    
    # For future use
    is_active = models.BooleanField(
        default=True, 
        verbose_name='সক্রিয়',
        help_text='ডাক্তার তালিকায় দেখানো হবে কিনা'
    )
    
    # Analytics
    view_count = models.IntegerField(
        default=0,
        verbose_name='ভিউ সংখ্যা',
        help_text='মোট কতবার ডাক্তার প্রোফাইল দেখা হয়েছে'
    )
    
    # Emergency Fields
    is_emergency_available = models.BooleanField(
        default=False,
        verbose_name='জরুরি সেবা উপলব্ধ',
        help_text='জরুরি প্রয়োজনে এই ডাক্তার পাওয়া যাবে কিনা'
    )
    is_24_7_available = models.BooleanField(
        default=False,
        verbose_name='২৪/৭ উপলব্ধ',
        help_text='২৪ ঘণ্টা সেবা দেন কিনা'
    )
    emergency_phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='জরুরি ফোন নম্বর',
        help_text='জরুরি যোগাযোগের ফোন নম্বর (ঐচ্ছিক)'
    )
    emergency_note = models.TextField(
        blank=True,
        verbose_name='জরুরি নোট',
        help_text='জরুরি সেবা সম্পর্কিত বিশেষ তথ্য (ঐচ্ছিক)'
    )
    last_emergency_update = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='শেষ আপডেট',
        help_text='জরুরি তথ্য শেষ আপডেট হওয়ার সময়'
    )
    
    class Meta:
        verbose_name = 'ডাক্তার'
        verbose_name_plural = 'ডাক্তারগণ'
        ordering = ['-is_emergency_available', '-is_24_7_available', 'name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['specialty']),
            models.Index(fields=['hospital']),
            models.Index(fields=['is_emergency_available']),
            models.Index(fields=['is_24_7_available']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_clean_hospital(self):
        """Get hospital name without HTML tags"""
        return self.clean_text(self.hospital)
    
    def get_clean_specialty(self):
        """Get specialty without HTML tags"""
        return self.clean_text(self.specialty)
    
    def get_clean_contact(self):
        """Get contact info with commas instead of line breaks"""
        if not self.contact:
            return ''
        # Replace <br> tags with comma and space
        text = re.sub(r'<br\s*/?>', ', ', self.contact, flags=re.IGNORECASE)
        # Remove other HTML tags
        text = strip_tags(text)
        # Clean up multiple spaces
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    @staticmethod
    def clean_text(text):
        """Remove HTML tags and normalize whitespace"""
        if not text:
            return ''
        text = re.sub(r'<br\s*/?>', ' ', text, flags=re.IGNORECASE)
        text = strip_tags(text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def get_category(self):
        """
        Get primary category or first assigned category
        Returns: Category name in Bengali
        """
        if self.primary_category:
            return self.primary_category.name
        
        first_category = self.categories.filter(is_active=True).first()
        if first_category:
            return first_category.name
        
        # Fallback to old method for backwards compatibility
        specialty_lower = self.specialty.lower() if self.specialty else ''
        
        for category, keywords in self.CATEGORY_MAPPING.items():
            for keyword in keywords:
                if keyword.lower() in specialty_lower:
                    return category
        
        return 'অন্যান্য বিশেষজ্ঞ'
    
    def auto_assign_categories(self):
        """
        Specialty থেকে automatically category assign করবে
        """
        if not self.specialty:
            return
        
        specialty_lower = self.specialty.lower()
        assigned_categories = []
        
        # Find matching categories based on keywords
        for keyword_obj in CategoryKeyword.objects.filter(is_active=True).select_related('category'):
            if keyword_obj.keyword.lower() in specialty_lower:
                if keyword_obj.category.is_active and keyword_obj.category not in assigned_categories:
                    assigned_categories.append(keyword_obj.category)
        
        # Assign categories if found
        if assigned_categories:
            self.categories.set(assigned_categories)
            
            # Set primary category if not already set
            if not self.primary_category:
                self.primary_category = assigned_categories[0]
                self.save(update_fields=['primary_category'])
    
    image = models.ImageField(
        upload_to='doctor_images/',
        blank=True,
        null=True,
        verbose_name='প্রোফাইল ছবি',
        help_text='ডাক্তারের ছবি (না দিলে ডিফল্ট ছবি দেখাবে)'
    )


class Favorite(models.Model):
    """User's favorite doctors"""
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        verbose_name='ইউজার'
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        verbose_name='ডাক্তার'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='যোগ করার সময়'
    )
    
    class Meta:
        verbose_name = 'পছন্দের ডাক্তার'
        verbose_name_plural = 'পছন্দের ডাক্তারগণ'
        unique_together = ['user', 'doctor']
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username} - {self.doctor.name}'


class Review(models.Model):
    """Doctor reviews and ratings"""
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        verbose_name='ইউজার'
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='ডাক্তার'
    )
    rating = models.IntegerField(
        choices=[(1, '১'), (2, '২'), (3, '৩'), (4, '৪'), (5, '৫')],
        verbose_name='রেটিং'
    )
    comment = models.TextField(
        verbose_name='মন্তব্য',
        help_text='আপনার অভিজ্ঞতা লিখুন'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='রিভিউ করার সময়'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='আপডেট করার সময়'
    )
    
    class Meta:
        verbose_name = 'রিভিউ'
        verbose_name_plural = 'রিভিউসমূহ'
        unique_together = ['user', 'doctor']
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username} - {self.doctor.name} ({self.rating}★)'


class TimeSlot(models.Model):
    """ডাক্তারের সময়সূচী স্লট"""
    DAYS_OF_WEEK = [
        ('saturday', 'শনিবার'),
        ('sunday', 'রবিবার'),
        ('monday', 'সোমবার'),
        ('tuesday', 'মঙ্গলবার'),
        ('wednesday', 'বুধবার'),
        ('thursday', 'বৃহস্পতিবার'),
        ('friday', 'শুক্রবার'),
    ]
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='time_slots')
    day_of_week = models.CharField('সপ্তাহের দিন', max_length=20, choices=DAYS_OF_WEEK)
    start_time = models.TimeField('শুরুর সময়')
    end_time = models.TimeField('শেষ সময়')
    is_available = models.BooleanField('উপলব্ধ', default=True)
    max_appointments = models.IntegerField('সর্বোচ্চ এপয়েন্টমেন্ট', default=5)
    
    class Meta:
        verbose_name = 'সময়সূচী'
        verbose_name_plural = 'সময়সূচীসমূহ'
        ordering = ['day_of_week', 'start_time']
    
    def __str__(self):
        return f'{self.doctor.name} - {self.get_day_of_week_display()} ({self.start_time}-{self.end_time})'


class Appointment(models.Model):
    """রোগীর এপয়েন্টমেন্ট"""
    STATUS_CHOICES = [
        ('pending', 'অপেক্ষমাণ'),
        ('confirmed', 'নিশ্চিত'),
        ('cancelled', 'বাতিল'),
        ('completed', 'সম্পন্ন'),
    ]
    
    patient = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField('এপয়েন্টমেন্টের তারিখ')
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    
    # Patient Information
    patient_name = models.CharField('রোগীর নাম', max_length=200)
    patient_age = models.IntegerField('রোগীর বয়স')
    patient_phone = models.CharField('ফোন নম্বর', max_length=20)
    problem_description = models.TextField('সমস্যার বিবরণ')
    
    # Status
    status = models.CharField('স্ট্যাটাস', max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField('তৈরি হয়েছে', auto_now_add=True)
    updated_at = models.DateTimeField('আপডেট হয়েছে', auto_now=True)
    
    # Admin notes
    admin_notes = models.TextField('অ্যাডমিন নোট', blank=True, null=True)
    
    class Meta:
        verbose_name = 'এপয়েন্টমেন্ট'
        verbose_name_plural = 'এপয়েন্টমেন্টসমূহ'
        ordering = ['-appointment_date', '-created_at']
        unique_together = ['doctor', 'appointment_date', 'time_slot']
    
    def __str__(self):
        return f'{self.patient_name} - {self.doctor.name} ({self.appointment_date})'


class DoctorView(models.Model):
    """ডাক্তার প্রোফাইল ভিউ ট্র্যাকিং"""
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='views',
        verbose_name='ডাক্তার'
    )
    viewed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='দেখার সময়'
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='আইপি ঠিকানা'
    )
    user_agent = models.TextField(
        blank=True,
        verbose_name='ব্রাউজার তথ্য'
    )
    referrer = models.URLField(
        blank=True,
        max_length=500,
        verbose_name='রেফারার'
    )
    session_key = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='সেশন কী'
    )
    
    class Meta:
        ordering = ['-viewed_at']
        verbose_name = 'ডাক্তার ভিউ'
        verbose_name_plural = 'ডাক্তার ভিউসমূহ'
        indexes = [
            models.Index(fields=['doctor', '-viewed_at']),
            models.Index(fields=['ip_address', 'viewed_at']),
            models.Index(fields=['-viewed_at']),
        ]
    
    def __str__(self):
        return f'{self.doctor.name} - {self.viewed_at.strftime("%Y-%m-%d %H:%M")}'


class SearchQuery(models.Model):
    """সার্চ কোয়েরি ট্র্যাকিং"""
    query = models.CharField(
        max_length=255,
        verbose_name='সার্চ টার্ম'
    )
    result_count = models.IntegerField(
        default=0,
        verbose_name='ফলাফল সংখ্যা'
    )
    searched_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='সার্চের সময়'
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='আইপি ঠিকানা'
    )
    category_filter = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='ক্যাটেগরি ফিল্টার'
    )
    clicked_doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='search_clicks',
        verbose_name='ক্লিক করা ডাক্তার'
    )
    
    class Meta:
        ordering = ['-searched_at']
        verbose_name = 'সার্চ কোয়েরি'
        verbose_name_plural = 'সার্চ কোয়েরিসমূহ'
        indexes = [
            models.Index(fields=['-searched_at']),
            models.Index(fields=['query']),
        ]
    
    def __str__(self):
        return f'"{self.query}" - {self.result_count} ফলাফল'


class DailyStats(models.Model):
    """দৈনিক পরিসংখ্যান"""
    date = models.DateField(
        unique=True,
        verbose_name='তারিখ'
    )
    total_views = models.IntegerField(
        default=0,
        verbose_name='মোট ভিউ'
    )
    unique_visitors = models.IntegerField(
        default=0,
        verbose_name='ইউনিক ভিজিটর'
    )
    total_searches = models.IntegerField(
        default=0,
        verbose_name='মোট সার্চ'
    )
    unique_searches = models.IntegerField(
        default=0,
        verbose_name='ইউনিক সার্চ'
    )
    most_viewed_doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='daily_stats_as_top',
        verbose_name='সর্বাধিক দেখা ডাক্তার'
    )
    most_searched_term = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='সর্বাধিক সার্চ টার্ম'
    )
    
    class Meta:
        ordering = ['-date']
        verbose_name = 'দৈনিক পরিসংখ্যান'
        verbose_name_plural = 'দৈনিক পরিসংখ্যানসমূহ'
        indexes = [
            models.Index(fields=['-date']),
        ]
    
    def __str__(self):
        return f'{self.date} - {self.total_views} ভিউ'
