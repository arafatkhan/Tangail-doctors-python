# 📅 Appointment System - বিস্তারিত পরিকল্পনা

এই ডকুমেন্টে টাঙ্গাইল ডাক্তার ডিরেক্টরি প্রজেক্টে **Appointment System** যুক্ত করার সম্পূর্ণ পরিকল্পনা রয়েছে।

---

## 🎯 প্রধান উদ্দেশ্য (Main Objectives)

1. রোগীরা অনলাইনে ডাক্তারের কাছে এপয়েন্টমেন্ট নিতে পারবে
2. ডাক্তার/অ্যাডমিন এপয়েন্টমেন্ট approve/reject/reschedule করতে পারবে
3. রোগী তার এপয়েন্টমেন্ট history দেখতে পারবে
4. এপয়েন্টমেন্ট status notification/alert পাবে
5. Time slot management এবং booking conflict prevention

---

## 🗂️ Features List

### ✅ Patient (রোগী) Features:
- [ ] Doctor profile থেকে "Book Appointment" button
- [ ] Date এবং time slot selection
- [ ] Appointment booking form (name, age, problem description, phone)
- [ ] Appointment confirmation message
- [ ] My Appointments page (upcoming, past, cancelled)
- [ ] Cancel appointment option
- [ ] Appointment status tracking (Pending → Confirmed/Rejected)

### ✅ Doctor/Admin Features:
- [ ] Admin panel থেকে appointment list দেখা
- [ ] Appointment approve/reject করা
- [ ] Available time slots configure করা
- [ ] Date-wise appointment calendar view
- [ ] Appointment details view
- [ ] Patient contact information access

### ✅ System Features:
- [ ] Email/SMS notification (optional - ভবিষ্যতে)
- [ ] Automatic slot blocking after booking
- [ ] Conflict detection (same doctor, same time)
- [ ] Past appointment archive
- [ ] Statistics (total appointments, confirmed, cancelled)

---

## 🗄️ Database Models

### 1. **TimeSlot Model**
```python
class TimeSlot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=20)  # Saturday, Sunday, etc.
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    max_appointments = models.IntegerField(default=5)  # per slot
```

### 2. **Appointment Model**
```python
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'অপেক্ষমাণ'),
        ('confirmed', 'নিশ্চিত'),
        ('cancelled', 'বাতিল'),
        ('completed', 'সম্পন্ন'),
    ]
    
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.SET_NULL, null=True)
    
    # Patient Information
    patient_name = models.CharField(max_length=200)
    patient_age = models.IntegerField()
    patient_phone = models.CharField(max_length=20)
    problem_description = models.TextField()
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Admin notes
    admin_notes = models.TextField(blank=True, null=True)
```

---

## 🛤️ URLs Structure

```python
# Appointment URLs
path('doctor/<int:doctor_id>/book/', views.book_appointment, name='book_appointment'),
path('appointments/', views.my_appointments, name='my_appointments'),
path('appointment/<int:pk>/', views.appointment_detail, name='appointment_detail'),
path('appointment/<int:pk>/cancel/', views.cancel_appointment, name='cancel_appointment'),

# Admin URLs
path('admin/appointments/', views.admin_appointments, name='admin_appointments'),
path('admin/appointment/<int:pk>/approve/', views.approve_appointment, name='approve_appointment'),
path('admin/appointment/<int:pk>/reject/', views.reject_appointment, name='reject_appointment'),
path('admin/timeslots/', views.manage_timeslots, name='manage_timeslots'),
```

---

## 🖥️ Views (প্রধান Functions)

### Patient Views:
1. **`book_appointment(request, doctor_id)`**
   - GET: Show booking form with available dates and time slots
   - POST: Create appointment (status='pending')
   - Validation: Check slot availability, conflict detection

2. **`my_appointments(request)`**
   - @login_required
   - Show user's all appointments (filter by status)
   - Pagination

3. **`appointment_detail(request, pk)`**
   - Show single appointment details
   - Cancel button (if status='pending' or 'confirmed')

4. **`cancel_appointment(request, pk)`**
   - Update appointment status to 'cancelled'
   - Redirect to my_appointments

### Admin Views:
5. **`admin_appointments(request)`**
   - @staff_member_required
   - List all appointments with filter options
   - Date range, doctor, status filtering

6. **`approve_appointment(request, pk)`**
   - Change status to 'confirmed'
   - Add admin notes (optional)

7. **`reject_appointment(request, pk)`**
   - Change status to 'cancelled'
   - Add rejection reason

8. **`manage_timeslots(request)`**
   - CRUD operations for TimeSlot
   - Add/Edit/Delete slots for each doctor

---

## 🎨 Templates

### Patient Templates:
1. **`book_appointment.html`**
   - Doctor info at top
   - Date picker (calendar widget)
   - Time slot selection (radio buttons)
   - Patient information form
   - Submit button

2. **`my_appointments.html`**
   - Tabs: All, Upcoming, Past, Cancelled
   - Card view of appointments
   - Status badges (color-coded)
   - Action buttons (View Details, Cancel)

3. **`appointment_detail.html`**
   - Full appointment information
   - Doctor details
   - Patient details
   - Status history
   - Cancel button (conditional)

### Admin Templates:
4. **`admin_appointments.html`**
   - Filter sidebar (date, doctor, status)
   - Table view with sorting
   - Quick action buttons (Approve, Reject)
   - Search functionality

5. **`manage_timeslots.html`**
   - Doctor selection dropdown
   - Weekly schedule view
   - Add slot modal/form
   - Edit/Delete slots

---

## 🔄 User Flow

### Patient Appointment Booking:
```
1. Browse doctors → 2. Click "Book Appointment"
3. Select date → 4. Choose time slot
5. Fill form (name, age, phone, problem)
6. Submit → 7. Confirmation message
8. Status: "Pending" (waiting for approval)
9. Check "My Appointments" page
10. Receive approval → Status: "Confirmed"
```

### Admin Approval Process:
```
1. Login to admin panel
2. Go to "Appointments" section
3. View pending appointments
4. Review patient details
5. Click "Approve" or "Reject"
6. Add notes (optional)
7. Patient sees updated status
```

---

## 🔧 Technical Requirements

### Backend:
- Django forms for validation
- Timezone awareness (Bangladesh time)
- Query optimization (select_related, prefetch_related)
- Pagination for appointment lists
- Permission checks (@login_required, @staff_member_required)

### Frontend:
- Date picker widget (Bootstrap Datepicker or similar)
- Dynamic time slot loading (AJAX optional)
- Status badges with colors (Bootstrap)
- Responsive design for mobile booking
- Form validation (client-side + server-side)

### Database:
- Index on appointment_date for faster queries
- Unique constraint: doctor + appointment_date + time_slot
- Soft delete for appointments (keep history)

---

## 📊 Implementation Steps

### Phase 1: Basic Structure
1. Create TimeSlot and Appointment models
2. Run migrations
3. Add models to admin panel
4. Create basic views (book_appointment, my_appointments)
5. Create basic templates

### Phase 2: Booking System
1. Implement date and time slot selection
2. Add form validation
3. Conflict detection logic
4. Confirmation page/message
5. Test booking flow

### Phase 3: Admin Panel
1. Admin appointment list view
2. Approve/Reject functionality
3. TimeSlot management interface
4. Filter and search options
5. Statistics dashboard (optional)

### Phase 4: Polish & Enhancement
1. Add email notifications (optional)
2. SMS integration (optional)
3. Appointment reminders
4. Calendar view for doctors
5. Export appointments (CSV/PDF)

---

## 🚀 Future Enhancements (Optional)

- Payment integration (appointment fee)
- Video consultation booking
- Prescription upload after appointment
- Patient health records
- Appointment rating/feedback
- Recurring appointments
- Multi-language support (fully Bengali)

---

## ⚠️ Important Considerations

1. **Privacy**: রোগীর তথ্য সুরক্ষিত রাখা
2. **Scalability**: অনেক appointment handle করার ক্ষমতা
3. **User Experience**: সহজ এবং দ্রুত booking process
4. **Mobile Friendly**: মোবাইল থেকে সহজে booking করা যাবে
5. **Conflict Prevention**: একই time slot এ duplicate booking বন্ধ করা

---

**Status:** 📝 Planning Complete - Implementation এর জন্য প্রস্তুত

**Next Step:** আমাকে বলুন "শুরু করো" এবং আমি Phase 1 থেকে implementation শুরু করব!

**Estimated Time:** 
- Phase 1: 30-45 minutes
- Phase 2: 45-60 minutes  
- Phase 3: 30-45 minutes
- Phase 4: 30-45 minutes

**Total:** 2.5-3 hours for complete appointment system

---

**Created:** February 1, 2026  
**Author:** GitHub Copilot  
**Project:** টাঙ্গাইল ডাক্তার ডিরেক্টরি
