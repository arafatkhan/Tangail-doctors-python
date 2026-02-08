# Medical Test Calculator - Implementation Plan

## 📋 Overview
Medinova Medical Services Ltd এর জন্য একটি comprehensive Test Calculator তৈরি করা যাবে যেখানে users multiple tests select করতে পারবে এবং total cost calculate হবে।

## 🎯 Key Features

### 1. Test Selection System
- **Category-wise Organization**: 34টি categories (HEMATOLOGY, BIOCHEMISTRY, HORMONE, etc.)
- **243টি different tests** with individual prices
- **Multi-select functionality**: Multiple tests একসাথে select করা
- **Search functionality**: Test name দিয়ে search
- **Category filter**: Specific category থেকে test খুঁজে পাওয়া

### 2. Calculator Features
- **Real-time calculation**: Test select করলেই total update হবে
- **Individual test price display**
- **Subtotal per category**: Category wise price breakdown
- **Grand total**: সব tests এর মোট দাম
- **Package suggestions**: যদি একাধিক test select করা হয় যা কোনো package এ available
- **Discount system** (optional): Bulk test এর জন্য discount

### 3. User Interface Components
- **Test List View**: Searchable, filterable test list
- **Selected Tests Cart**: Shopping cart style display
- **Category Navigation**: Sidebar with categories
- **Price Summary Panel**: Right side fixed panel with total
- **Print/Export**: PDF download or print quotation

## 🏗️ Technical Architecture

### Option 1: Django App Integration (Recommended)
```
tangail-doctors-python/
├── tests/                      # New Django app
│   ├── models.py              # Test, TestCategory models
│   ├── views.py               # Calculator views
│   ├── urls.py                # Test calculator routes
│   ├── admin.py               # Admin interface
│   ├── management/
│   │   └── commands/
│   │       └── import_tests.py  # Import from JSON
│   ├── templates/
│   │   └── tests/
│   │       ├── calculator.html     # Main calculator page
│   │       ├── test_list.html      # Test listing
│   │       ├── quotation.html      # Printable quotation
│   └── static/
│       └── tests/
│           ├── css/
│           │   └── calculator.css
│           └── js/
│               └── calculator.js    # Interactive functionality
```

### Option 2: Standalone Web App
Single HTML/CSS/JavaScript application যা JSON file থেকে data load করবে।

## 📊 Database Models (Django Integration)

### TestCategory Model
```python
class TestCategory(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    order = models.IntegerField(default=0)
    icon = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['order', 'name']
```

### Test Model
```python
class Test(models.Model):
    test_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=300)
    category = models.ForeignKey(TestCategory)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    is_package = models.BooleanField(default=False)
    package_tests = models.ManyToManyField('self', blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['test_id']
```

### TestQuotation Model (Optional - Save quotations)
```python
class TestQuotation(models.Model):
    quotation_id = models.CharField(max_length=20, unique=True)
    patient_name = models.CharField(max_length=200, blank=True)
    tests = models.ManyToManyField(Test)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
```

## 🎨 UI/UX Design

### Layout Structure
```
┌─────────────────────────────────────────────────────────┐
│  Header: Medinova Test Calculator                       │
├──────────────┬──────────────────────────┬───────────────┤
│              │                          │               │
│  Category    │   Test List & Search     │  Calculator   │
│  Sidebar     │   ┌────────────────┐     │  Panel        │
│              │   │ Search Box     │     │               │
│  • HEMATOLOGY│   └────────────────┘     │  Selected: 5  │
│  • BIOCHEM   │                          │               │
│  • HORMONE   │   ☐ CBC (300 Tk)         │  ✓ CBC - 300  │
│  • CARDIAC   │   ☐ RBS (150 Tk)         │  ✓ RBS - 150  │
│  • ...       │   ☐ TSH (500 Tk)         │  ✓ TSH - 500  │
│              │   ...                    │               │
│              │                          │  Total: 950 Tk│
│              │                          │               │
│              │                          │  [Print]      │
└──────────────┴──────────────────────────┴───────────────┘
```

### Key UI Features
1. **Sticky Calculator Panel**: Always visible on right
2. **Category Highlight**: Active category highlighted
3. **Checkbox Selection**: Easy multi-select
4. **Remove Button**: Quick remove from cart
5. **Responsive Design**: Mobile-friendly layout
6. **Bengali Language Support**: All labels in Bengali
7. **Hover Effects**: Price highlight on hover
8. **Badge System**: Show package tests with badge

## 💻 Frontend Functionality (JavaScript)

### Core Functions
```javascript
// Test selection
function selectTest(testId, testName, price)
function removeTest(testId)
function clearAll()

// Calculation
function calculateSubtotal(category)
function calculateGrandTotal()
function applyDiscount(percentage)

// Package detection
function checkPackageAvailable(selectedTests)
function suggestPackage()

// Search & Filter
function searchTests(query)
function filterByCategory(categoryId)

// Export
function printQuotation()
function downloadPDF()
function shareWhatsApp()
```

### LocalStorage Integration
Selected tests কে localStorage এ save করা যাতে page refresh এ data না হারায়।

## 🔧 Implementation Steps

### Phase 1: Django App Setup (Day 1)
1. Create `tests` app
2. Create models (TestCategory, Test)
3. Create management command to import JSON data
4. Setup admin interface
5. Run migrations and import data

### Phase 2: Basic Calculator (Day 2)
1. Create calculator view
2. Design basic HTML template
3. Implement category sidebar
4. Create test listing with checkboxes
5. Build calculator panel

### Phase 3: Interactive Features (Day 3)
1. Implement JavaScript for real-time calculation
2. Add search functionality
3. Add category filtering
4. Implement localStorage for persistence
5. Add remove/clear functionality

### Phase 4: Advanced Features (Day 4)
1. Package detection and suggestions
2. Discount system
3. Print quotation functionality
4. PDF export
5. WhatsApp share feature

### Phase 5: UI Polish & Testing (Day 5)
1. Responsive design testing
2. Bengali language optimization
3. Loading animations
4. Error handling
5. Cross-browser testing

## 📱 Additional Features (Optional)

### 1. User Integration
- Link with User authentication
- Save quotations to user account
- View quotation history
- Favorite tests

### 2. Admin Features
- Update test prices from admin
- Add/remove tests dynamically
- Manage discount rules
- View quotation analytics

### 3. Appointment Integration
- Book appointment with selected tests
- Send quotation via email
- Integration with payment gateway

### 4. Home Collection
- Add home collection option
- Calculate home service charges
- Location-based pricing

### 5. Reports & Analytics
- Most popular tests
- Revenue by category
- Daily/monthly test statistics
- Export reports

## 🎯 Routes Structure

```python
# tests/urls.py
urlpatterns = [
    path('calculator/', views.calculator, name='calculator'),
    path('api/tests/', views.api_test_list, name='api_test_list'),
    path('api/search/', views.api_search, name='api_search'),
    path('api/calculate/', views.api_calculate, name='api_calculate'),
    path('quotation/<str:id>/', views.quotation_detail, name='quotation_detail'),
    path('quotation/<str:id>/pdf/', views.quotation_pdf, name='quotation_pdf'),
    path('quotation/save/', views.save_quotation, name='save_quotation'),
]
```

## 📦 Required Packages

```txt
# For PDF generation
reportlab==3.6.13
weasyprint==60.1

# For Excel export (optional)
openpyxl==3.1.2

# Already available in project
django==4.2.7
```

## 🎨 Design References

### Color Scheme (Medinova Medical)
- Primary: #0066CC (Medical Blue)
- Secondary: #00A859 (Health Green)
- Accent: #FF6B6B (Emergency Red)
- Background: #F8F9FA
- Text: #2C3E50

### Typography
- Headings: Hind Siliguri (Bengali font)
- Body: Noto Sans Bengali
- Numbers: Roboto

## 🚀 Quick Start Commands

```bash
# Create new app
python manage.py startapp tests

# Import test data
python manage.py import_tests

# Run server
python manage.py runserver

# Create superuser (if needed)
python manage.py createsuperuser
```

## 📋 Success Criteria

1. ✅ All 243 tests imported successfully
2. ✅ Category-wise organization working
3. ✅ Real-time price calculation accurate
4. ✅ Search functionality responsive (< 100ms)
5. ✅ Mobile responsive design
6. ✅ Print/PDF export working
7. ✅ Bengali language properly displayed
8. ✅ Data persistence (localStorage)
9. ✅ Package suggestions working
10. ✅ Admin panel fully functional

## 🎯 Future Enhancements

1. **AI-powered Test Suggestions**: Based on symptoms
2. **Lab Report Integration**: Upload and view reports
3. **Doctor Prescription Upload**: Automatic test extraction
4. **Insurance Coverage**: Show insurance covered tests
5. **Comparison Tool**: Compare prices with other labs
6. **Appointment Scheduling**: Book test appointment
7. **Home Collection**: Schedule sample collection
8. **Multi-language**: English, Bengali, others
9. **Mobile App**: React Native/Flutter app
10. **Payment Integration**: bKash, Nagad, card payment

---

## 📞 Contact Information
**Medinova Medical Services Ltd**  
Phone: 01921-232302, 01921-232303  
Location: Dhaka, Bangladesh

---

## 🎉 Ready to Start?
এই plan follow করে step-by-step implementation শুরু করা যাবে। আপনি যদি বলেন তাহলে আমি এখনই Phase 1 দিয়ে শুরু করব!
