from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import Doctor, Favorite, Review, TimeSlot, Appointment, Category
from .utils import record_doctor_view, record_search_query, get_popular_doctors
from datetime import datetime, timedelta, date

def index(request):
    """কার্ড ভিউ - সব ডাক্তার দেখাবে"""
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    doctors = Doctor.objects.filter(is_active=True)
    # সার্চ ফিল্টার
    if search_query:
        doctors = doctors.filter(
            Q(name__icontains=search_query) |
            Q(specialty__icontains=search_query) |
            Q(hospital__icontains=search_query) |
            Q(qualification__icontains=search_query)
        )
        # Track search query
        result_count = doctors.count()
        record_search_query(request, search_query, result_count, category_filter)
    # ক্যাটেগরি ফিল্টার (dynamic from database)
    if category_filter:
        doctors = doctors.filter(categories__slug=category_filter, categories__is_active=True).distinct()
    
    # Pagination
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    paginator = Paginator(doctors, 20)  # 20 doctors per page
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    # সব ক্যাটেগরি লিস্ট (from database)
    categories = Category.objects.filter(is_active=True).order_by('order', 'name')
    
    # Get popular doctors (only on first page, no search/filter)
    popular_doctors = []
    if not search_query and not category_filter and page_obj.number == 1:
        popular_doctors = get_popular_doctors(limit=5, days=30)
    
    context = {
        'doctors': page_obj.object_list,
        'page_obj': page_obj,
        'search_query': search_query,
        'category_filter': category_filter,
        'categories': categories,
        'popular_doctors': popular_doctors,
    }
    return render(request, 'doctors/index.html', context)

def table_view(request):
    """টেবিল ভিউ - ডাক্তারদের টেবিল ফরম্যাটে দেখাবে"""
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    doctors = Doctor.objects.filter(is_active=True)
    # সার্চ ফিল্টার
    if search_query:
        doctors = doctors.filter(
            Q(name__icontains=search_query) |
            Q(specialty__icontains=search_query) |
            Q(hospital__icontains=search_query) |
            Q(qualification__icontains=search_query)
        )
        # Track search query
        result_count = doctors.count()
        record_search_query(request, search_query, result_count, category_filter)
    # ক্যাটেগরি ফিল্টার (dynamic)
    if category_filter:
        doctors = doctors.filter(categories__slug=category_filter, categories__is_active=True).distinct()
    
    # Pagination
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    paginator = Paginator(doctors, 20)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    # সব ক্যাটেগরি লিস্ট (from database)
    categories = Category.objects.filter(is_active=True).order_by('order', 'name')
    context = {
        'doctors': page_obj.object_list,
        'page_obj': page_obj,
        'search_query': search_query,
        'category_filter': category_filter,
        'categories': categories,
    }
    return render(request, 'doctors/table.html', context)

def category_view(request, category_slug):
    """ক্যাটেগরি ভিউ - নির্দিষ্ট ক্যাটেগরির ডাক্তার দেখাবে"""
    # Get category from database
    category = get_object_or_404(Category, slug=category_slug, is_active=True)
    
    search_query = request.GET.get('search', '')
    
    # Get doctors in this category
    doctors = Doctor.objects.filter(
        categories=category,
        is_active=True
    ).distinct()
    
    # সার্চ ফিল্টার
    if search_query:
        doctors = doctors.filter(
            Q(name__icontains=search_query) |
            Q(specialty__icontains=search_query) |
            Q(hospital__icontains=search_query)
        )
        # Track search query
        result_count = doctors.count()
        record_search_query(request, search_query, result_count, category_slug)
    
    # Pagination
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    paginator = Paginator(doctors, 20)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    # সব ক্যাটেগরি লিস্ট (from database)
    categories = Category.objects.filter(is_active=True).order_by('order', 'name')
    
    context = {
        'doctors': page_obj.object_list,
        'page_obj': page_obj,
        'search_query': search_query,
        'category_slug': category_slug,
        'category_name': category.name,
        'categories': categories,
    }
    return render(request, 'doctors/category.html', context)

def doctor_detail(request, pk):
    """একক ডাক্তারের বিস্তারিত তথ্য"""
    doctor = get_object_or_404(Doctor, pk=pk, is_active=True)
    
    # Record view
    record_doctor_view(request, doctor)
    
    # Check if user has favorited this doctor
    is_favorited = False
    user_review = None
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, doctor=doctor).exists()
        user_review = Review.objects.filter(user=request.user, doctor=doctor).first()
    
    # Get all reviews for this doctor
    reviews = Review.objects.filter(doctor=doctor).select_related('user')
    
    context = {
        'doctor': doctor,
        'is_favorited': is_favorited,
        'user_review': user_review,
        'reviews': reviews,
    }
    return render(request, 'doctors/detail.html', context)


def hospital_list(request):
    """হাসপাতাল তালিকা - প্রতিটি হাসপাতালে কতজন ডাক্তার আছে"""
    from django.db.models import Count, Max
    
    search_query = request.GET.get('search', '')
    
    # Get all unique hospitals with doctor count, exclude empty hospital names
    # Group only by hospital name to avoid duplicates
    hospitals = Doctor.objects.filter(
        is_active=True
    ).exclude(
        hospital__isnull=True
    ).exclude(
        hospital__exact=''
    )
    
    # Apply search filter
    if search_query:
        hospitals = hospitals.filter(
            Q(hospital__icontains=search_query) |
            Q(hospital_address__icontains=search_query)
        )
    
    hospitals = hospitals.values(
        'hospital'
    ).annotate(
        doctor_count=Count('id'),
        hospital_address=Max('hospital_address')  # Get one address (any non-null)
    ).order_by('hospital')
    
    # Pagination
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    paginator = Paginator(hospitals, 20)  # 20 hospitals per page
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    context = {
        'hospitals': page_obj.object_list,
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'doctors/hospital_list.html', context)


def hospital_doctors(request, hospital_name):
    """নির্দিষ্ট হাসপাতালের সব ডাক্তার"""
    doctors = Doctor.objects.filter(
        hospital=hospital_name,
        is_active=True
    )
    
    hospital_address = doctors.first().hospital_address if doctors.exists() else ''
    
    # Pagination
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    paginator = Paginator(doctors, 20)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    context = {
        'hospital_name': hospital_name,
        'hospital_address': hospital_address,
        'doctors': page_obj.object_list,
        'page_obj': page_obj,
    }
    return render(request, 'doctors/hospital_doctors.html', context)


# User Authentication Views
def register_view(request):
    """ইউজার রেজিস্ট্রেশন"""
    if request.user.is_authenticated:
        return redirect('doctors:index')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'আপনার একাউন্ট তৈরি হয়েছে!')
            return redirect('doctors:index')
    else:
        form = UserCreationForm()
    
    return render(request, 'doctors/register.html', {'form': form})


def login_view(request):
    """ইউজার লগইন"""
    if request.user.is_authenticated:
        return redirect('doctors:index')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'স্বাগতম {username}!')
                return redirect('doctors:index')
    else:
        form = AuthenticationForm()
    
    return render(request, 'doctors/login.html', {'form': form})


def logout_view(request):
    """ইউজার লগআউট"""
    logout(request)
    messages.info(request, 'আপনি লগআউট করেছেন')
    return redirect('doctors:index')


@login_required
def profile_view(request):
    """ইউজার প্রোফাইল"""
    favorites = Favorite.objects.filter(user=request.user).select_related('doctor')
    reviews = Review.objects.filter(user=request.user).select_related('doctor')
    
    context = {
        'favorites': favorites,
        'reviews': reviews,
    }
    return render(request, 'doctors/profile.html', context)


@login_required
def add_favorite(request, doctor_id):
    """ফেভারিট যোগ করুন"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, doctor=doctor)
    
    if created:
        messages.success(request, f'{doctor.name} ফেভারিটে যোগ হয়েছে')
    else:
        messages.info(request, 'এটি ইতিমধ্যে ফেভারিটে আছে')
    
    return redirect('doctors:detail', pk=doctor_id)


@login_required
def remove_favorite(request, doctor_id):
    """ফেভারিট সরান"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    favorite = Favorite.objects.filter(user=request.user, doctor=doctor).first()
    
    if favorite:
        favorite.delete()
        messages.success(request, f'{doctor.name} ফেভারিট থেকে সরানো হয়েছে')
    
    return redirect('doctors:detail', pk=doctor_id)


@login_required
def add_review(request, doctor_id):
    """রিভিউ যোগ করুন"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if rating and comment:
            review, created = Review.objects.update_or_create(
                user=request.user,
                doctor=doctor,
                defaults={'rating': rating, 'comment': comment}
            )
            if created:
                messages.success(request, 'রিভিউ যোগ হয়েছে')
            else:
                messages.success(request, 'রিভিউ আপডেট হয়েছে')
        else:
            messages.error(request, 'রেটিং এবং কমেন্ট দিন')
    
    return redirect('doctors:detail', pk=doctor_id)


@staff_member_required
def edit_doctor(request, pk):
    """সুপার অ্যাডমিন ডাক্তারের তথ্য এডিট করতে পারবে"""
    doctor = get_object_or_404(Doctor, pk=pk)
    
    if request.method == 'POST':
        # Update doctor information
        doctor.name = request.POST.get('name', doctor.name)
        doctor.qualification = request.POST.get('qualification', doctor.qualification)
        doctor.specialty = request.POST.get('specialty', doctor.specialty)
        doctor.schedule = request.POST.get('schedule', doctor.schedule)
        doctor.hospital = request.POST.get('hospital', doctor.hospital)
        doctor.contact = request.POST.get('contact', doctor.contact)
        
        # Handle image upload
        if 'image' in request.FILES:
            doctor.image = request.FILES['image']
        
        doctor.save()
        messages.success(request, 'ডাক্তারের তথ্য সফলভাবে আপডেট হয়েছে')
        return redirect('doctors:detail', pk=doctor.pk)
    
    context = {
        'doctor': doctor,
    }
    return render(request, 'doctors/edit_doctor.html', context)


@login_required
def book_appointment(request, doctor_id):
    """এপয়েন্টমেন্ট বুকিং করুন"""
    doctor = get_object_or_404(Doctor, pk=doctor_id, is_active=True)
    
    # Get available time slots for this doctor
    time_slots = TimeSlot.objects.filter(doctor=doctor, is_available=True)
    
    if request.method == 'POST':
        appointment_date = request.POST.get('appointment_date')
        time_slot_id = request.POST.get('time_slot')
        patient_name = request.POST.get('patient_name')
        patient_age = request.POST.get('patient_age')
        patient_phone = request.POST.get('patient_phone')
        problem_description = request.POST.get('problem_description')
        
        # Validation
        if not all([appointment_date, time_slot_id, patient_name, patient_age, patient_phone, problem_description]):
            messages.error(request, 'সব তথ্য পূরণ করুন')
            return redirect('doctors:book_appointment', doctor_id=doctor_id)
        
        try:
            time_slot = TimeSlot.objects.get(pk=time_slot_id, doctor=doctor)
            appointment_date_obj = datetime.strptime(appointment_date, '%Y-%m-%d').date()
            
            # Check if date is in the past
            if appointment_date_obj < date.today():
                messages.error(request, 'অতীতের তারিখে এপয়েন্টমেন্ট নেওয়া যাবে না')
                return redirect('doctors:book_appointment', doctor_id=doctor_id)
            
            # Check for existing appointment (conflict detection)
            existing = Appointment.objects.filter(
                doctor=doctor,
                appointment_date=appointment_date_obj,
                time_slot=time_slot,
                status__in=['pending', 'confirmed']
            ).count()
            
            if existing >= time_slot.max_appointments:
                messages.error(request, 'এই সময়ে আর এপয়েন্টমেন্ট উপলব্ধ নেই')
                return redirect('doctors:book_appointment', doctor_id=doctor_id)
            
            # Create appointment
            appointment = Appointment.objects.create(
                patient=request.user,
                doctor=doctor,
                appointment_date=appointment_date_obj,
                time_slot=time_slot,
                patient_name=patient_name,
                patient_age=patient_age,
                patient_phone=patient_phone,
                problem_description=problem_description,
                status='pending'
            )
            
            messages.success(request, 'এপয়েন্টমেন্ট সফলভাবে বুক করা হয়েছে। অনুমোদনের জন্য অপেক্ষা করুন।')
            return redirect('doctors:my_appointments')
            
        except TimeSlot.DoesNotExist:
            messages.error(request, 'সময়সূচী পাওয়া যায়নি')
        except ValueError:
            messages.error(request, 'তারিখ ফরম্যাট সঠিক নয়')
        except Exception as e:
            messages.error(request, f'ত্রুটি: {str(e)}')
        
        return redirect('doctors:book_appointment', doctor_id=doctor_id)
    
    context = {
        'doctor': doctor,
        'time_slots': time_slots,
        'today': date.today().isoformat(),
    }
    return render(request, 'doctors/book_appointment.html', context)


@login_required
def my_appointments(request):
    """আমার এপয়েন্টমেন্টসমূহ"""
    status_filter = request.GET.get('status', 'all')
    
    appointments = Appointment.objects.filter(patient=request.user).select_related('doctor', 'time_slot')
    
    # Filter by status
    if status_filter != 'all':
        appointments = appointments.filter(status=status_filter)
    
    # Pagination
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    paginator = Paginator(appointments, 10)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    context = {
        'appointments': page_obj.object_list,
        'page_obj': page_obj,
        'status_filter': status_filter,
    }
    return render(request, 'doctors/my_appointments.html', context)


@login_required
def cancel_appointment(request, appointment_id):
    """এপয়েন্টমেন্ট বাতিল করুন"""
    appointment = get_object_or_404(Appointment, pk=appointment_id, patient=request.user)
    
    if appointment.status in ['pending', 'confirmed']:
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, 'এপয়েন্টমেন্ট বাতিল করা হয়েছে')
    else:
        messages.error(request, 'এই এপয়েন্টমেন্ট বাতিল করা যাবে না')
    
    return redirect('doctors:my_appointments')
