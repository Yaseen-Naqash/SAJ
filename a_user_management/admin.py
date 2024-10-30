from django.contrib import admin
from .models import Student, Teacher, Person, PhoneVerification, Grade, Employee
from a_course_management.models import Section, HomeWork, HomeWorkDocument, Exam, ExamDocument
import django_jalali.admin as jadmin # jalali date picker
from django.db import models  
from django.contrib.auth.models import Group
from SAJ.custom_permissions import AdminPermissionMixin


class SectionStudentInline(admin.TabularInline):
    model = Section.students.through  
    extra = 0


# TEACHER
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 
        'last_name', 
        'phone', 
        'code_melli'
    )
    
    search_fields = ['first_name', 'last_name', 'phone', 'code_melli']  # Define searchable fields for Student

    formfield_overrides = {
        models.DateField: {'widget': jadmin.widgets.AdminjDateWidget},  # Use Jalali date picker in admin
    }
admin.site.register(Teacher)


admin.site.register(PhoneVerification)
admin.site.register(Grade)
admin.site.register(Employee)














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
        'code_melli', 
        'grade',
        'balance_status',
    )
    
    list_filter = (
        'education',
        'grade',
        'ageLevel',
        'activity',
        'branch',
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


    inlines = [SectionStudentInline]


