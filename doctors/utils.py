# -*- coding: utf-8 -*-
"""
Utility functions for doctors app
"""
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Q, Sum


def get_client_ip(request):
    """
    Get client IP address from request
    Handles proxy/load balancer scenarios
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def record_doctor_view(request, doctor):
    """
    Record a doctor profile view
    Prevents duplicate views from same session within 5 minutes
    """
    from .models import DoctorView
    
    # Get IP address
    ip_address = get_client_ip(request)
    
    # Get or create session key
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    
    # Check for recent view from same session
    five_minutes_ago = timezone.now() - timedelta(minutes=5)
    recent_view = DoctorView.objects.filter(
        doctor=doctor,
        session_key=session_key,
        viewed_at__gte=five_minutes_ago
    ).exists()
    
    # Don't record duplicate view
    if recent_view:
        return None
    
    # Get user agent and referrer
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    referrer = request.META.get('HTTP_REFERER', '')
    
    # Create view record
    view = DoctorView.objects.create(
        doctor=doctor,
        ip_address=ip_address,
        user_agent=user_agent,
        referrer=referrer,
        session_key=session_key
    )
    
    # Update doctor view count
    doctor.view_count = doctor.views.count()
    doctor.save(update_fields=['view_count'])
    
    return view


def record_search_query(request, query, result_count, category_filter=''):
    """
    Record a search query
    """
    from .models import SearchQuery
    
    # Get IP address
    ip_address = get_client_ip(request)
    
    # Create search record
    search = SearchQuery.objects.create(
        query=query,
        result_count=result_count,
        ip_address=ip_address,
        category_filter=category_filter
    )
    
    return search


def get_popular_doctors(limit=10, days=30):
    """
    Get most viewed doctors in last N days
    """
    from .models import Doctor
    
    start_date = timezone.now() - timedelta(days=days)
    
    return Doctor.objects.filter(
        is_active=True
    ).annotate(
        recent_views=Count('views', filter=Q(views__viewed_at__gte=start_date))
    ).order_by('-recent_views', '-view_count')[:limit]


def get_popular_searches(limit=10, days=30):
    """
    Get most frequent search queries in last N days
    """
    from .models import SearchQuery
    
    start_date = timezone.now() - timedelta(days=days)
    
    return SearchQuery.objects.filter(
        searched_at__gte=start_date
    ).values('query').annotate(
        count=Count('id')
    ).order_by('-count')[:limit]


def get_category_stats():
    """
    Get view statistics by category
    """
    from .models import Category
    
    return Category.objects.filter(
        is_active=True
    ).annotate(
        total_views=Sum('doctors__view_count'),
        doctor_count=Count('doctors', filter=Q(doctors__is_active=True))
    ).order_by('-total_views')


def get_trending_doctors(limit=10, days=7):
    """
    Get trending doctors (most views in recent days)
    """
    from .models import Doctor
    
    start_date = timezone.now() - timedelta(days=days)
    
    return Doctor.objects.filter(
        is_active=True
    ).annotate(
        recent_views=Count('views', filter=Q(views__viewed_at__gte=start_date))
    ).filter(
        recent_views__gt=0
    ).order_by('-recent_views')[:limit]
