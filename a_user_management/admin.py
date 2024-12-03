from django.contrib import admin
from .models import Student, Teacher, Person, PhoneVerification, Grade, Employee, Manager, Owner
from a_course_management.models import Section, HomeWork, HomeWorkDocument, Exam, ExamDocument
from a_financial_management.models import Receipt
import django_jalali.admin as jadmin # jalali date picker
from django.db import models  
from django.contrib.auth.models import Group
from SAJ.custom_permissions import AdminPermissionMixin
from django.urls import reverse
from django.utils.html import format_html


class SectionStudentInline(admin.TabularInline):
    model = Section.students.through  
    extra = 0
    autocomplete_fields = ['section']

class ReceiptInline(admin.TabularInline):
    model = Receipt
    extra = 0
    exclude  = ['description', 'sender_account', 'receiver_account', 'transaction_id']  # Only these fields will be shown.


# TEACHER
@admin.register(Teacher)
class TeacherAdmin(AdminPermissionMixin, admin.ModelAdmin):
    list_display = (
        'first_name', 
        'last_name', 
        'phone',
        'code_melli',
    )
    
    search_fields = ['first_name', 'last_name', 'phone', 'code_melli']  # Define searchable fields for Student

    formfield_overrides = {
        models.DateField: {'widget': jadmin.widgets.AdminjDateWidget},  # Use Jalali date picker in admin
    }


# admin.site.register(PhoneVerification)
# admin.site.register(Grade)

@admin.register(Employee)
class EmployeeAdmin(AdminPermissionMixin, admin.ModelAdmin):
    list_display = (
        'first_name', 
        'last_name', 
        'phone',
        'code_melli',
    )
    
    search_fields = ['first_name', 'last_name', 'phone', 'code_melli']  # Define searchable fields for Student

    formfield_overrides = {
        models.DateField: {'widget': jadmin.widgets.AdminjDateWidget},  # Use Jalali date picker in admin
    }



    # Custom filter class for student balance
class BalanceStatusFilter(admin.SimpleListFilter):
    title = ('وضعیت موجودی')  # The title displayed in the filter section
    parameter_name = 'balance_status'  # The URL parameter for the filter

    # Define filter options (dropdown choices)
    def lookups(self, request, model_admin):
        return [
            ('positive', ('بستانکار')),
            ('negative', ('بدهکار')),
            ('zero', ('بی حساب')),
        ]

    # Define how the queryset is filtered based on the selected option
    def queryset(self, request, queryset):
        if self.value() == 'positive':
            return queryset.filter(balance__gt=0)
        elif self.value() == 'negative':
            return queryset.filter(balance__lt=0)
        elif self.value() == 'zero':
            return queryset.filter(balance=0)
        return queryset


#STUDENT
@admin.register(Student)
class StudentAdmin(AdminPermissionMixin, admin.ModelAdmin):

    list_display = (
        'first_name', 
        'last_name', 
        'phone', 
        'latest_course_title',
        'formatted_balance',
        'view_receipts_link',
    )
    readonly_fields = ('latest_course_title',)

    
    def latest_course_title(self, obj):
        return obj.latest_course_title
    latest_course_title.short_description = "آخرین دوره قبول شده"
    
    def formatted_balance(self, obj):
        # Format the balance with commas and color based on its value
        balance = obj.balance
        formatted = f"{abs(balance):,}"  # Add commas to the balance value remove = sign from value
        if balance > 0:
            return format_html('<span style="color: #2cff05;">{}</span>', formatted)
        elif balance < 0:
            return format_html('<span style="color: #ff2c2c;">{}</span>', formatted)
        else:
            return '0'  # No special color for zero balance

    formatted_balance.short_description = 'موجودی (تومان)'
    
    def view_receipts_link(self, obj):
        url = reverse('admin:a_financial_management_receipt_changelist') + f'?payer__id__exact={obj.id}'
        return format_html('<a href="{}">اطلاعات مالی</a>', url)

    view_receipts_link.short_description = "اطلاعات مالی"
    
    list_filter = (
        'education',
        'grade',
        'ageLevel',
        'activity',
        'branch',
        'gender',
        BalanceStatusFilter,
        
    )

    search_fields = ['first_name', 'last_name', 'phone', 'code_melli']  # Define searchable fields for Student


    
    def balance_status(self, obj):
        if obj.balance > 0:
            return 'بستانکار'
        elif obj.balance < 0:
            return 'بدهکار'
        else:
            return 'بی حساب'
    
    balance_status.short_description = 'موجودی' 

    # THIS IS WHAT TO APPLY TO ADD A JALALI DATE PICKER IN ADMIN PANEL
    formfield_overrides = {
        models.DateField: {'widget': jadmin.widgets.AdminjDateWidget},  # Use Jalali date picker in admin
    }


    inlines = [SectionStudentInline,]



    # HANDLES PERMISSION OF SHWOING THE ADD RECEIPTS FOR THAT STUDENT 
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        # Check if the user has permission to add a Receipt
        extra_context['can_add_receipt'] = request.user.has_perm("a_financial_management.add_receipt")
        return super().change_view(request, object_id, form_url, extra_context=extra_context)



#MANAGER
@admin.register(Manager)
class ManagerAdmin(AdminPermissionMixin, admin.ModelAdmin):


    list_display = (
        'first_name', 
        'last_name', 
        'phone', 
    )

#OWNER
@admin.register(Owner)
class OwnerAdmin(AdminPermissionMixin, admin.ModelAdmin):


    list_display = (
        'first_name', 
        'last_name', 
        'phone', 
    )
