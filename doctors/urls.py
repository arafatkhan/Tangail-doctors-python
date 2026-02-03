from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    path('', views.index, name='index'),
    path('table/', views.table_view, name='table'),
    path('emergency/', views.emergency_doctors, name='emergency'),
    path('category/<str:category_slug>/', views.category_view, name='category'),
    path('doctor/<int:pk>/', views.doctor_detail, name='detail'),
    path('hospitals/', views.hospital_list, name='hospital_list'),
    path('hospital/<str:hospital_name>/', views.hospital_doctors, name='hospital_doctors'),
    
    # Authentication URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    
    # Favorite and Review URLs
    path('doctor/<int:doctor_id>/favorite/add/', views.add_favorite, name='add_favorite'),
    path('doctor/<int:doctor_id>/favorite/remove/', views.remove_favorite, name='remove_favorite'),
    path('doctor/<int:doctor_id>/review/add/', views.add_review, name='add_review'),
    
    # Admin edit URL
    path('doctor/<int:pk>/edit/', views.edit_doctor, name='edit_doctor'),
    
    # Appointment URLs
    path('doctor/<int:doctor_id>/book/', views.book_appointment, name='book_appointment'),
    path('appointments/', views.my_appointments, name='my_appointments'),
    path('appointment/<int:appointment_id>/cancel/', views.cancel_appointment, name='cancel_appointment'),
]
