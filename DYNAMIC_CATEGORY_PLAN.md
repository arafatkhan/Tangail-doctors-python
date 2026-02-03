# 🏷️ Dynamic Category Management - বিস্তারিত পরিকল্পনা

এই ডকুমেন্টে টাঙ্গাইল ডাক্তার ডিরেক্টরি প্রজেক্টে **Dynamic Category Management** যুক্ত করার সম্পূর্ণ পরিকল্পনা রয়েছে।

---

## 🎯 প্রধান সমস্যা (Current Problem)

বর্তমানে `Doctor` model এ category mapping hardcoded করা আছে:

```python
CATEGORY_MAPPING = {
    'প্রসূতি ও স্ত্রীরোগ বিশেষজ্ঞ': ['প্রসূতি', 'স্ত্রী', 'গাইনী', ...],
    'সার্জারি বিশেষজ্ঞ': ['সার্জন', 'সার্জারি', ...],
    ...
}
```

**সীমাবদ্ধতা:**
- নতুন category add করতে code edit করতে হয়
- Category rename/delete করা যায় না
- Keywords update করতে code change দরকার
- Admin panel থেকে manage করা যায় না
- Deployment এর পর category পরিবর্তন কঠিন

---

## 🎯 প্রধান উদ্দেশ্য (Main Objectives)

1. Admin panel থেকে category dynamically add/edit/delete করা যাবে
2. প্রতিটি category এর জন্য keywords manage করা যাবে
3. Doctor কে multiple categories assign করা যাবে (many-to-many)
4. Category-based filtering এবং navigation আরও flexible হবে
5. Category icon/color customization option থাকবে
6. Category statistics (কত ডাক্তার আছে) automatically calculate হবে

---

## 🗂️ Features List

### ✅ Admin Features:
- [ ] Category CRUD operations (Create, Read, Update, Delete)
- [ ] Category name (Bengali + English)
- [ ] Category icon selection (Font Awesome)
- [ ] Category color/badge color customization
- [ ] Keywords management (comma-separated বা separate model)
- [ ] Category ordering/priority
- [ ] Active/Inactive status for categories
- [ ] Bulk assign doctors to categories

### ✅ Doctor Features:
- [ ] Multiple categories per doctor (many-to-many relationship)
- [ ] Auto-categorize based on specialty keywords
- [ ] Manual category override option
- [ ] Primary category selection (main category)

### ✅ Frontend Features:
- [ ] Dynamic category navigation bar
- [ ] Category cards with doctor count
- [ ] Category filter on all pages
- [ ] Category-wise color coding
- [ ] Search within category
- [ ] Empty category handling (hide if no doctors)

---

## 🗄️ Database Models

### 1. **Category Model** (নতুন)
```python
class Category(models.Model):
    name = models.CharField('নাম', max_length=100, unique=True)
    name_english = models.CharField('English Name', max_length=100, blank=True)
    slug = models.SlugField('স্লাগ', unique=True)
    description = models.TextField('বিবরণ', blank=True)
    icon = models.CharField('আইকন', max_length=50, default='fa-stethoscope')
    color = models.CharField('রং', max_length=20, default='primary')
    order = models.IntegerField('ক্রম', default=0)
    is_active = models.BooleanField('সক্রিয়', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'ক্যাটেগরি'
        verbose_name_plural = 'ক্যাটেগরিসমূহ'
    
    def __str__(self):
        return self.name
    
    def get_doctor_count(self):
        return self.doctors.filter(is_active=True).count()
```

### 2. **CategoryKeyword Model** (নতুন)
```python
class CategoryKeyword(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='keywords')
    keyword = models.CharField('কীওয়ার্ড', max_length=100)
    is_active = models.BooleanField('সক্রিয়', default=True)
    
    class Meta:
        unique_together = ['category', 'keyword']
        verbose_name = 'ক্যাটেগরি কীওয়ার্ড'
        verbose_name_plural = 'ক্যাটেগরি কীওয়ার্ডসমূহ'
    
    def __str__(self):
        return f'{self.category.name} - {self.keyword}'
```

### 3. **Doctor Model Update** (পরিবর্তন)
```python
class Doctor(models.Model):
    # ... existing fields ...
    
    # Replace CATEGORY_MAPPING with:
    categories = models.ManyToManyField(
        Category, 
        related_name='doctors',
        blank=True,
        verbose_name='ক্যাটেগরিসমূহ'
    )
    primary_category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='primary_doctors',
        verbose_name='প্রধান ক্যাটেগরি'
    )
    
    # Remove get_category() method
    # Add new method:
    def auto_assign_categories(self):
        """Specialty থেকে automatically category assign করবে"""
        if not self.specialty:
            return
        
        specialty_lower = self.specialty.lower()
        assigned_categories = []
        
        for keyword_obj in CategoryKeyword.objects.filter(is_active=True).select_related('category'):
            if keyword_obj.keyword.lower() in specialty_lower:
                if keyword_obj.category.is_active:
                    assigned_categories.append(keyword_obj.category)
        
        if assigned_categories:
            self.categories.set(assigned_categories)
            if not self.primary_category and assigned_categories:
                self.primary_category = assigned_categories[0]
            self.save()
```

---

## 🛤️ URLs Structure

```python
# Category Management URLs
path('categories/', views.category_list, name='category_list'),
path('category/<slug:slug>/', views.category_detail, name='category_detail'),

# Admin URLs (already covered by Django admin)
# Optional: Custom category management pages
path('admin/category/assign/', views.admin_assign_categories, name='admin_assign_categories'),
```

---

## 🖥️ Views (প্রধান Functions)

### 1. **`category_list(request)`**
   - সব active categories দেখাবে
   - প্রতিটি category তে কত ডাক্তার আছে
   - Grid/Card layout
   - Search functionality

### 2. **`category_detail(request, slug)`**
   - নির্দিষ্ট category এর সব ডাক্তার
   - Category info display
   - Filtering and pagination
   - Replace current category_view()

### 3. **`admin_assign_categories(request)`** (Optional)
   - @staff_member_required
   - Bulk category assignment
   - Auto-categorize all doctors button
   - Preview before apply

---

## 🎨 Templates

### 1. **`category_list.html`**
   - Grid of category cards
   - Category icon, name, doctor count
   - Color-coded badges
   - Search bar
   - "View All Doctors" link per category

### 2. **`category_detail.html`**
   - Category banner with description
   - Doctor list (can reuse existing templates)
   - Subcategory navigation (if applicable)
   - Back to categories link

### 3. **Base template updates**
   - Dynamic category navigation menu
   - Replace hardcoded category buttons
   - Load categories from database

---

## 🔄 Migration Strategy

### Phase 1: Create New Models
1. Create Category and CategoryKeyword models
2. Run migrations
3. Add to admin panel

### Phase 2: Data Migration
1. Create management command to migrate existing hardcoded categories
2. Convert CATEGORY_MAPPING to database entries
3. Auto-assign categories to existing doctors

```python
# Management command: migrate_categories.py
class Command(BaseCommand):
    def handle(self, *args, **options):
        # Create categories from CATEGORY_MAPPING
        for category_name, keywords in Doctor.CATEGORY_MAPPING.items():
            category, created = Category.objects.get_or_create(
                name=category_name,
                defaults={
                    'slug': slugify(category_name),
                    'icon': 'fa-stethoscope',
                    'color': 'primary',
                }
            )
            
            # Add keywords
            for keyword in keywords:
                CategoryKeyword.objects.get_or_create(
                    category=category,
                    keyword=keyword
                )
        
        # Auto-assign categories to all doctors
        for doctor in Doctor.objects.all():
            doctor.auto_assign_categories()
```

### Phase 3: Update Code
1. Update views to use Category model
2. Update templates with dynamic categories
3. Remove hardcoded CATEGORY_MAPPING
4. Update filtering logic

### Phase 4: Testing
1. Test category CRUD operations
2. Test doctor categorization
3. Test filtering and navigation
4. Test edge cases (no category, multiple categories)

---

## 📊 Admin Panel Enhancements

### Category Admin:
```python
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'color', 'order', 'is_active', 'get_doctor_count']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'name_english', 'description']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    
    def get_doctor_count(self, obj):
        return obj.get_doctor_count()
    get_doctor_count.short_description = 'ডাক্তার সংখ্যা'
```

### CategoryKeyword Inline:
```python
class CategoryKeywordInline(admin.TabularInline):
    model = CategoryKeyword
    extra = 3
```

### Doctor Admin Update:
```python
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    # Add to list_display:
    list_display = [..., 'primary_category', 'get_categories']
    
    # Add filter:
    list_filter = [..., 'categories', 'primary_category']
    
    # Add to fieldsets:
    fieldsets = (
        ...
        ('ক্যাটেগরি', {
            'fields': ('categories', 'primary_category')
        }),
    )
    
    filter_horizontal = ['categories']
    
    actions = ['auto_assign_categories']
    
    def auto_assign_categories(self, request, queryset):
        for doctor in queryset:
            doctor.auto_assign_categories()
        self.message_user(request, f'{queryset.count()}জন ডাক্তারের ক্যাটেগরি আপডেট হয়েছে')
    auto_assign_categories.short_description = 'স্বয়ংক্রিয় ক্যাটেগরি নির্ধারণ'
```

---

## 🔧 Technical Considerations

### 1. **Backwards Compatibility**
- Keep existing URLs working during migration
- Redirect old category URLs to new slugs
- Maintain get_category() method temporarily

### 2. **Performance**
- Index on category slug
- Cache category list
- Use select_related() for queries
- Prefetch doctor counts

### 3. **Validation**
- Prevent duplicate category names
- Validate slug uniqueness
- Check circular dependencies
- Ensure at least one category per doctor (optional)

### 4. **Icon Selection**
- Store Font Awesome class name (e.g., 'fa-heart')
- Provide icon picker in admin (or dropdown)
- Default icons for common categories

### 5. **Color Options**
- Bootstrap colors: primary, success, danger, warning, info, secondary
- Or custom hex colors
- Preview in admin panel

---

## 📊 Implementation Steps

### Phase 1: Database Structure (30-45 min)
1. ✅ Create Category model
2. ✅ Create CategoryKeyword model
3. ✅ Add ManyToMany to Doctor model
4. ✅ Run migrations
5. ✅ Add to admin panel

### Phase 2: Data Migration (30 min)
1. ✅ Create management command
2. ✅ Migrate hardcoded categories to database
3. ✅ Auto-assign categories to existing doctors
4. ✅ Verify data integrity

### Phase 3: Views & Templates (45-60 min)
1. ✅ Update category_list view
2. ✅ Update category_detail view
3. ✅ Create/update templates
4. ✅ Update navigation menu
5. ✅ Update filtering logic

### Phase 4: Testing & Cleanup (30 min)
1. ✅ Test all category operations
2. ✅ Test doctor categorization
3. ✅ Remove hardcoded CATEGORY_MAPPING
4. ✅ Update documentation
5. ✅ Performance testing

---

## 🚀 Future Enhancements (Optional)

- **Hierarchical Categories**: Parent-child category relationships
- **Category Tags**: Additional tags beyond main categories
- **Category Images**: Banner images for category pages
- **Popular Categories**: Track view counts
- **Suggested Categories**: ML-based category suggestion
- **Multi-language Support**: Category names in multiple languages
- **Category SEO**: Meta descriptions, keywords for categories

---

## ⚠️ Important Considerations

1. **Data Integrity**: ডাক্তারদের existing categorization ঠিক থাকবে
2. **URL Structure**: Existing category URLs redirect করতে হবে
3. **User Experience**: Category navigation সহজ এবং intuitive হবে
4. **Admin Usability**: Admin panel থেকে সহজে manage করা যাবে
5. **Performance**: বড় category list efficiently load হবে

---

## 📝 Benefits of Dynamic Categories

✅ **Flexibility**: নতুন category সহজে add করা যাবে  
✅ **Maintainability**: Code change ছাড়াই category manage করা যাবে  
✅ **Scalability**: Category system বাড়ানো সহজ হবে  
✅ **User-Friendly**: Admin panel থেকে সব কিছু control করা যাবে  
✅ **Accuracy**: Doctor categorization আরও accurate হবে  
✅ **Professional**: More polished and professional approach  

---

**Status:** 📝 Planning Complete - Implementation এর জন্য প্রস্তুত

**Next Step:** আমাকে বলুন এবং আমি Phase 1 থেকে implementation শুরু করব!

**Estimated Time:** 
- Phase 1: 30-45 minutes
- Phase 2: 30 minutes  
- Phase 3: 45-60 minutes
- Phase 4: 30 minutes

**Total:** 2-3 hours for complete dynamic category system

---

**Created:** February 2, 2026  
**Author:** GitHub Copilot  
**Project:** টাঙ্গাইল ডাক্তার ডিরেক্টরি
