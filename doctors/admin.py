from django.contrib import admin
from .models import Doctor, Favorite, Review, TimeSlot, Appointment, Category, CategoryKeyword, DoctorView, SearchQuery, DailyStats

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialty_short', 'hospital', 'get_category', 'get_categories_list', 'is_emergency_available', 'is_24_7_available', 'view_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'is_emergency_available', 'is_24_7_available', 'hospital', 'created_at', 'categories', 'primary_category']
    search_fields = ['name', 'specialty', 'hospital', 'qualification', 'contact', 'hospital_address', 'emergency_phone']
    list_editable = ['is_active', 'is_emergency_available', 'is_24_7_available']
    date_hierarchy = 'created_at'
    ordering = ['-is_emergency_available', '-is_24_7_available', '-view_count', 'hospital', '-created_at']
    list_per_page = 50
    filter_horizontal = ['categories']
    
    fieldsets = (
        ('মূল তথ্য', {
            'fields': ('name', 'qualification', 'specialty', 'image')
        }),
        ('হাসপাতাল তথ্য', {
            'fields': ('hospital', 'hospital_address')
        }),
        ('ক্যাটেগরি', {
            'fields': ('categories', 'primary_category')
        }),
        ('যোগাযোগ তথ্য', {
            'fields': ('contact', 'schedule')
        }),
        ('জরুরি সেবা', {
            'fields': ('is_emergency_available', 'is_24_7_available', 'emergency_phone', 'emergency_note', 'last_emergency_update'),
            'classes': ('collapse',),
            'description': 'জরুরি চিকিৎসা সেবার জন্য এই তথ্য ব্যবহার করা হবে'
        }),
        ('অবস্থা', {
            'fields': ('is_active',)
        }),
    )
    
    actions = ['auto_assign_categories_action']
    
    def specialty_short(self, obj):
        """বিশেষত্ব সংক্ষিপ্ত"""
        return obj.get_clean_specialty()[:50] + '...' if len(obj.get_clean_specialty()) > 50 else obj.get_clean_specialty()
    specialty_short.short_description = 'বিশেষত্ব'
    
    def get_category(self, obj):
        """প্রধান ক্যাটেগরি"""
        return obj.get_category()
    get_category.short_description = 'প্রধান ক্যাটেগরি'
    
    def get_categories_list(self, obj):
        """সব ক্যাটেগরি"""
        categories = obj.categories.filter(is_active=True)
        if categories.exists():
            return ', '.join([cat.name for cat in categories[:3]])
        return '-'
    get_categories_list.short_description = 'ক্যাটেগরিসমূহ'
    
    def auto_assign_categories_action(self, request, queryset):
        """Bulk action: স্বয়ংক্রিয় ক্যাটেগরি নির্ধারণ"""
        count = 0
        for doctor in queryset:
            doctor.auto_assign_categories()
            count += 1
        self.message_user(request, f'{count}জন ডাক্তারের ক্যাটেগরি আপডেট হয়েছে')
    auto_assign_categories_action.short_description = 'স্বয়ংক্রিয় ক্যাটেগরি নির্ধারণ'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'doctor', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'doctor__name']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    def has_add_permission(self, request):
        # Prevent adding favorites from admin (should be done from frontend)
        return False


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'doctor', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'doctor__name', 'comment']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('রিভিউ তথ্য', {
            'fields': ('user', 'doctor', 'rating', 'comment')
        }),
        ('সময়', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'day_of_week', 'start_time', 'end_time', 'max_appointments', 'is_available']
    list_filter = ['day_of_week', 'is_available', 'doctor']
    search_fields = ['doctor__name']
    list_editable = ['is_available', 'max_appointments']
    ordering = ['doctor', 'day_of_week', 'start_time']
    list_per_page = 50
    
    fieldsets = (
        ('ডাক্তার তথ্য', {
            'fields': ('doctor',)
        }),
        ('সময়সূচী', {
            'fields': ('day_of_week', 'start_time', 'end_time')
        }),
        ('সেটিংস', {
            'fields': ('max_appointments', 'is_available')
        }),
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'doctor', 'appointment_date', 'time_slot', 'status', 'created_at']
    list_filter = ['status', 'appointment_date', 'created_at', 'doctor']
    search_fields = ['patient_name', 'patient_phone', 'doctor__name', 'problem_description']
    date_hierarchy = 'appointment_date'
    ordering = ['-appointment_date', '-created_at']
    list_per_page = 50
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('রোগীর তথ্য', {
            'fields': ('patient', 'patient_name', 'patient_age', 'patient_phone')
        }),
        ('এপয়েন্টমেন্ট তথ্য', {
            'fields': ('doctor', 'appointment_date', 'time_slot', 'problem_description')
        }),
        ('স্ট্যাটাস', {
            'fields': ('status', 'admin_notes')
        }),
        ('সময়', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_appointments', 'reject_appointments', 'mark_completed']
    
    def approve_appointments(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated}টি এপয়েন্টমেন্ট নিশ্চিত করা হয়েছে')
    approve_appointments.short_description = 'নির্বাচিত এপয়েন্টমেন্ট নিশ্চিত করুন'
    
    def reject_appointments(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated}টি এপয়েন্টমেন্ট বাতিল করা হয়েছে')
    reject_appointments.short_description = 'নির্বাচিত এপয়েন্টমেন্ট বাতিল করুন'
    
    def mark_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated}টি এপয়েন্টমেন্ট সম্পন্ন করা হয়েছে')
    mark_completed.short_description = 'নির্বাচিত এপয়েন্টমেন্ট সম্পন্ন করুন'


class CategoryKeywordInline(admin.TabularInline):
    """Category এর Keywords inline editing"""
    model = CategoryKeyword
    extra = 3
    fields = ['keyword', 'is_active']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_english', 'slug', 'icon', 'color', 'order', 'is_active', 'get_doctor_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'name_english', 'description']
    list_editable = ['order', 'is_active', 'color']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
    list_per_page = 50
    inlines = [CategoryKeywordInline]
    
    fieldsets = (
        ('মূল তথ্য', {
            'fields': ('name', 'name_english', 'slug')
        }),
        ('বিবরণ', {
            'fields': ('description',)
        }),
        ('স্টাইল', {
            'fields': ('icon', 'color')
        }),
        ('সেটিংস', {
            'fields': ('order', 'is_active')
        }),
        ('সময়', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_doctor_count(self, obj):
        return obj.get_doctor_count()
    get_doctor_count.short_description = 'ডাক্তার সংখ্যা'


@admin.register(CategoryKeyword)
class CategoryKeywordAdmin(admin.ModelAdmin):
    list_display = ['category', 'keyword', 'is_active']
    list_filter = ['is_active', 'category']
    search_fields = ['keyword', 'category__name']
    list_editable = ['is_active']
    ordering = ['category', 'keyword']
    list_per_page = 100


@admin.register(DoctorView)
class DoctorViewAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'viewed_at', 'ip_address', 'session_key_short']
    list_filter = ['viewed_at']
    search_fields = ['doctor__name', 'ip_address']
    date_hierarchy = 'viewed_at'
    readonly_fields = ['doctor', 'viewed_at', 'ip_address', 'user_agent', 'referrer', 'session_key']
    ordering = ['-viewed_at']
    list_per_page = 100
    
    def session_key_short(self, obj):
        """Show first 10 characters of session key"""
        return obj.session_key[:10] + '...' if len(obj.session_key) > 10 else obj.session_key
    session_key_short.short_description = 'সেশন'
    
    def has_add_permission(self, request):
        """Don't allow manual addition of views"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Don't allow editing of views"""
        return False


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ['query', 'result_count', 'searched_at', 'ip_address', 'category_filter', 'clicked_doctor']
    list_filter = ['searched_at', 'result_count', 'category_filter']
    search_fields = ['query', 'ip_address']
    date_hierarchy = 'searched_at'
    readonly_fields = ['query', 'result_count', 'searched_at', 'ip_address', 'category_filter', 'clicked_doctor']
    ordering = ['-searched_at']
    list_per_page = 100
    
    def has_add_permission(self, request):
        """Don't allow manual addition of searches"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Don't allow editing of searches"""
        return False


@admin.register(DailyStats)
class DailyStatsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_views', 'unique_visitors', 'total_searches', 'unique_searches', 'most_viewed_doctor', 'most_searched_term']
    list_filter = ['date']
    search_fields = ['most_searched_term', 'most_viewed_doctor__name']
    date_hierarchy = 'date'
    readonly_fields = ['date', 'total_views', 'unique_visitors', 'total_searches', 'unique_searches', 'most_viewed_doctor', 'most_searched_term']
    ordering = ['-date']
    list_per_page = 100
    
    def has_add_permission(self, request):
        """Don't allow manual addition - use management command"""
        return False
