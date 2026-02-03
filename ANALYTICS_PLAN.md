# 📊 Analytics System Implementation Plan

## উদ্দেশ্য (Objective)
Doctor view count, statistics tracking, popular doctor ranking, search analytics, এবং category-wise statistics implement করা যাতে admin panel থেকে সব analytics দেখা যায় এবং user experience উন্নত হয়।

---

## ✨ Features to Implement

### 1. **Doctor View Tracking**
- প্রতিটি doctor profile view count track করা
- View history (date, time, IP) সংরক্ষণ
- Unique visitor vs total views আলাদা করা
- Daily, Weekly, Monthly view statistics

### 2. **Popular Doctor Rankings**
- View count অনুযায়ী most viewed doctors
- Category-wise popular doctors
- Trending doctors (recent views based)
- Top doctors dashboard widget

### 3. **Search Analytics**
- Search queries track করা
- Search result count tracking
- Popular search terms
- Zero result searches tracking
- Search conversion rate (search → doctor view)

### 4. **Category Statistics**
- Category-wise doctor distribution
- Category-wise view counts
- Popular categories ranking
- Category growth tracking

### 5. **Admin Dashboard**
- Overview statistics (total views, doctors, categories)
- Charts and graphs (view trends, popular categories)
- Export analytics data (CSV/Excel)
- Date range filtering

---

## 🗂️ Database Models

### 1. **DoctorView Model**
```python
class DoctorView(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='views')
    viewed_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(blank=True, max_length=500)
    session_key = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['-viewed_at']
        indexes = [
            models.Index(fields=['doctor', '-viewed_at']),
            models.Index(fields=['ip_address', 'viewed_at']),
        ]
```

### 2. **SearchQuery Model**
```python
class SearchQuery(models.Model):
    query = models.CharField(max_length=255)
    result_count = models.IntegerField(default=0)
    searched_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    category_filter = models.CharField(max_length=100, blank=True)
    clicked_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-searched_at']
        indexes = [
            models.Index(fields=['-searched_at']),
            models.Index(fields=['query']),
        ]
```

### 3. **DailyStats Model**
```python
class DailyStats(models.Model):
    date = models.DateField(unique=True)
    total_views = models.IntegerField(default=0)
    unique_visitors = models.IntegerField(default=0)
    total_searches = models.IntegerField(default=0)
    unique_searches = models.IntegerField(default=0)
    most_viewed_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    most_searched_term = models.CharField(max_length=255, blank=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Daily Statistics"
```

---

## 📝 Implementation Phases

### **Phase 1: Models & Migrations**
1. ✅ Create DoctorView model
2. ✅ Create SearchQuery model
3. ✅ Create DailyStats model
4. ✅ Add view_count field to Doctor model (for quick access)
5. ✅ Create and apply migrations

### **Phase 2: View Tracking**
1. ✅ Create middleware to track doctor views
2. ✅ Implement IP-based unique visitor detection
3. ✅ Add session-based view tracking
4. ✅ Create utility function to record view
5. ✅ Update doctor detail view to track views

### **Phase 3: Search Tracking**
1. ✅ Update search views to log queries
2. ✅ Track result count for each search
3. ✅ Track clicked doctors from search results
4. ✅ Implement search conversion tracking

### **Phase 4: Statistics Aggregation**
1. ✅ Create management command for daily stats calculation
2. ✅ Implement scheduled task (cron/celery) for daily aggregation
3. ✅ Add methods to calculate popular doctors
4. ✅ Add methods to calculate category statistics

### **Phase 5: Admin Dashboard**
1. ✅ Create analytics admin views
2. ✅ Add charts using Chart.js or similar
3. ✅ Implement date range filtering
4. ✅ Add export functionality (CSV)
5. ✅ Create dashboard widgets

### **Phase 6: Public Display**
1. ✅ Show view count on doctor detail page
2. ✅ Display "Popular Doctors" section on homepage
3. ✅ Add "Trending Now" widget
4. ✅ Show category popularity indicators

---

## 🔧 Technical Implementation

### 1. **View Tracking Middleware**
```python
# doctors/middleware.py
class DoctorViewMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Track doctor views from detail page
        if hasattr(request, 'doctor_to_track'):
            self._record_view(request, request.doctor_to_track)
        
        return response
    
    def _record_view(self, request, doctor):
        # Get IP and user agent
        # Check for duplicate views (same session within timeframe)
        # Create DoctorView entry
        pass
```

### 2. **Doctor Model Updates**
```python
class Doctor(models.Model):
    # ... existing fields ...
    view_count = models.IntegerField(default=0)
    
    def get_view_count(self):
        """Get total view count"""
        return self.views.count()
    
    def get_unique_visitors(self):
        """Get unique visitor count"""
        return self.views.values('ip_address').distinct().count()
    
    def get_views_by_date_range(self, start_date, end_date):
        """Get views within date range"""
        return self.views.filter(viewed_at__range=[start_date, end_date])
```

### 3. **Analytics Utility Functions**
```python
# doctors/utils/analytics.py

def get_popular_doctors(limit=10, days=30):
    """Get most viewed doctors in last N days"""
    from datetime import timedelta
    from django.utils import timezone
    
    start_date = timezone.now() - timedelta(days=days)
    return Doctor.objects.annotate(
        recent_views=Count('views', filter=Q(views__viewed_at__gte=start_date))
    ).order_by('-recent_views')[:limit]

def get_popular_searches(limit=10, days=30):
    """Get most frequent search queries"""
    from datetime import timedelta
    from django.utils import timezone
    
    start_date = timezone.now() - timedelta(days=days)
    return SearchQuery.objects.filter(
        searched_at__gte=start_date
    ).values('query').annotate(
        count=Count('id')
    ).order_by('-count')[:limit]

def get_category_stats():
    """Get view statistics by category"""
    return Category.objects.annotate(
        total_views=Sum('doctors__view_count'),
        doctor_count=Count('doctors', filter=Q(doctors__is_active=True))
    ).order_by('-total_views')
```

### 4. **Management Command for Daily Aggregation**
```python
# doctors/management/commands/aggregate_daily_stats.py

class Command(BaseCommand):
    def handle(self, *args, **options):
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        
        # Calculate yesterday's stats
        total_views = DoctorView.objects.filter(
            viewed_at__date=yesterday
        ).count()
        
        unique_visitors = DoctorView.objects.filter(
            viewed_at__date=yesterday
        ).values('ip_address').distinct().count()
        
        # Find most viewed doctor
        most_viewed = Doctor.objects.annotate(
            daily_views=Count('views', filter=Q(views__viewed_at__date=yesterday))
        ).order_by('-daily_views').first()
        
        # Save stats
        DailyStats.objects.update_or_create(
            date=yesterday,
            defaults={
                'total_views': total_views,
                'unique_visitors': unique_visitors,
                'most_viewed_doctor': most_viewed,
                # ... other stats
            }
        )
```

### 5. **Admin Dashboard Views**
```python
# doctors/admin.py

@admin.register(DoctorView)
class DoctorViewAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'viewed_at', 'ip_address']
    list_filter = ['viewed_at', 'doctor']
    search_fields = ['doctor__name', 'ip_address']
    date_hierarchy = 'viewed_at'
    
@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ['query', 'result_count', 'searched_at', 'category_filter']
    list_filter = ['searched_at', 'result_count']
    search_fields = ['query']
    date_hierarchy = 'searched_at'

@admin.register(DailyStats)
class DailyStatsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_views', 'unique_visitors', 'total_searches', 'most_viewed_doctor']
    list_filter = ['date']
    date_hierarchy = 'date'
```

---

## 📊 Analytics Dashboard Features

### 1. **Overview Cards**
- Total Views (today, this week, this month)
- Unique Visitors
- Total Searches
- Active Doctors

### 2. **Charts**
- Views trend (line chart - last 30 days)
- Category distribution (pie chart)
- Popular doctors (bar chart)
- Search terms (word cloud)

### 3. **Tables**
- Top 10 Doctors (by views)
- Recent Searches
- Zero Result Searches
- Popular Search Terms

### 4. **Filters**
- Date range picker
- Category filter
- Doctor filter
- Export options

---

## 🎯 Performance Considerations

### 1. **Database Indexing**
- Index on `viewed_at` for date-based queries
- Index on `doctor_id` for doctor-specific queries
- Index on `ip_address` for unique visitor calculation
- Composite index on (doctor, viewed_at)

### 2. **Caching**
```python
from django.core.cache import cache

def get_popular_doctors_cached(limit=10):
    cache_key = f'popular_doctors_{limit}'
    result = cache.get(cache_key)
    
    if result is None:
        result = get_popular_doctors(limit=limit)
        cache.set(cache_key, result, 60 * 60)  # Cache for 1 hour
    
    return result
```

### 3. **Aggregation Optimization**
- Use `select_related()` and `prefetch_related()`
- Aggregate data daily to reduce real-time calculations
- Use database views for complex queries

### 4. **Data Retention Policy**
- Keep detailed views for 90 days
- Archive older data to separate table
- Keep aggregated stats indefinitely

---

## 🚀 Additional Features (Optional)

### 1. **Real-time Analytics**
- WebSocket-based live view counter
- Real-time visitor count on admin dashboard
- Live search query stream

### 2. **Advanced Analytics**
- Bounce rate calculation
- Average time on page
- Referrer analysis
- Geographic distribution (if location data available)

### 3. **Comparative Analytics**
- Compare doctors side-by-side
- Period-over-period comparison
- Category comparison

### 4. **Export & Reports**
- PDF report generation
- Email scheduled reports
- CSV/Excel export with charts

---

## 📋 Implementation Checklist

- [ ] Create DoctorView, SearchQuery, DailyStats models
- [ ] Add view_count to Doctor model
- [ ] Create and apply migrations
- [ ] Implement view tracking middleware
- [ ] Update doctor detail view to record views
- [ ] Implement search query logging
- [ ] Create analytics utility functions
- [ ] Create daily aggregation management command
- [ ] Set up scheduled task (cron)
- [ ] Register models in admin panel
- [ ] Create analytics dashboard view
- [ ] Add charts and visualizations
- [ ] Implement date range filtering
- [ ] Add export functionality
- [ ] Display popular doctors on homepage
- [ ] Show view count on doctor cards
- [ ] Test performance with sample data
- [ ] Add caching for frequently accessed stats
- [ ] Create documentation

---

## 🔒 Privacy Considerations

1. **IP Address Storage**
   - Hash IP addresses for privacy
   - Allow users to opt-out of tracking
   - Comply with GDPR/privacy regulations

2. **Data Anonymization**
   - Remove personal identifiers after aggregation
   - Don't store sensitive user data

3. **Transparency**
   - Add privacy policy
   - Inform users about tracking
   - Provide data deletion option

---

## 📚 Dependencies

```txt
# For charts and visualizations
django-chartjs==2.3.0
# or
plotly==5.18.0

# For scheduled tasks
celery==5.3.4
django-celery-beat==2.5.0

# For export functionality
openpyxl==3.1.2
reportlab==4.0.7

# For IP geolocation (optional)
geoip2==4.7.0
```

---

## 🎓 Learning Resources

- Django Aggregation: https://docs.djangoproject.com/en/4.2/topics/db/aggregation/
- Chart.js: https://www.chartjs.org/
- Celery: https://docs.celeryproject.org/
- Django Caching: https://docs.djangoproject.com/en/4.2/topics/cache/

---

**Created:** February 2, 2026  
**Status:** Planning Phase  
**Priority:** Medium-High (6th in roadmap after Dynamic Category)

---

## 📌 Notes

- Analytics implementation করার সময় performance-এর দিকে বিশেষ নজর দিতে হবে
- বড় data volume handle করার জন্য proper indexing এবং caching essential
- Privacy policy এবং GDPR compliance ensure করতে হবে
- Real-time tracking এর জন্য WebSocket বা similar technology ব্যবহার করা যেতে পারে
