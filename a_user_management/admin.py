from django.contrib import admin
from .models import Student, Teacher, Person, PhoneVerification, Grade, Employee
from a_course_management.models import Section, HomeWork, HomeWorkDocument, Exam, ExamDocument
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin
from django.db import models  
from django.contrib.auth.models import Group


class SectionStudentInline(admin.TabularInline):
    model = Section.students.through  
    extra = 1


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





class CustomAdminMixin:
    """
    Mixin to provide different querysets and field access based on the user's group.
    """

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Admins see all data
        if request.user.is_superuser:
            return qs
        
        # Employees see only certain data
        if request.user.groups.filter(name="کارمند").exists():
            return qs.filter()  # Apply appropriate filter for Employee

        # TEACHERS see only their data
        if qs.model == HomeWork:
                # If the queryset is for HomeWork model, filter by teacher field
            return qs.filter(teacher=request.user.teacher)
            
        elif qs.model == Student:
                # If the queryset is for Student model, filter by section's teacher
            return qs.filter(sections__teacher=request.user.teacher).distinct()
        
        # Default to no data if no valid group
        return qs.none()

    # def get_readonly_fields(self, request, obj=None):
    #     # Admins can edit all fields
    #     if request.user.is_superuser or request.user.groups.filter(name="Admin").exists():
    #         return []
        
    #     # Employees can edit some fields but not all
    #     if request.user.groups.filter(name="Employee").exists():
    #         return ['field1', 'field2']  # Fields that should be readonly for Employee
        
    #     # Teachers can edit a subset of fields
    #     if request.user.groups.filter(name="Teacher").exists():
    #         return ['field3', 'field4']  # Fields that should be readonly for Teacher
        
    #     # By default, make all fields read-only
    #     return self.fields

    # def get_fieldsets(self, request, obj=None):
    #     # Custom fieldsets based on group
    #     if request.user.is_superuser or request.user.groups.filter(name="Admin").exists():
    #         return super().get_fieldsets(request, obj)
        
    #     if request.user.groups.filter(name="کارمند").exists():
    #         # Fieldsets for Employee
    #         return (
    #             (None, {
    #                 'fields': ('field1', 'field2', 'field3')  # Allow employees to see certain fields
    #             }),
    #         )
        
    #     if request.user.groups.filter(name="استاد").exists():
    #         # Fieldsets for Teacher
    #         return (
    #             (None, {
    #                 'fields': ('field3', 'field4')  # Allow teachers to see only certain fields
    #             }),
    #         )
        
    #     # Default: no fieldsets (in case of error)
    #     return super().get_fieldsets(request, obj)
    
        


    #STUDENT

@admin.register(Student)
class StudentAdmin(CustomAdminMixin, admin.ModelAdmin):

    list_display = (
        'first_name', 
        'last_name', 
        'phone', 
        'code_melli', 
        'grade',
    )
    
    list_filter = (
        'education',
        'grade',
        'ageLevel',
        'activity',
        'branch',
    )

    search_fields = ['first_name', 'last_name', 'phone', 'code_melli']  # Define searchable fields for Student

    formfield_overrides = {
        models.DateField: {'widget': jadmin.widgets.AdminjDateWidget},  # Use Jalali date picker in admin
    }
    inlines = [SectionStudentInline]


    