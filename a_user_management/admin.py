from django.contrib import admin
from .models import Student, Teacher, Person, PhoneVerification, Grade, Employee
from a_course_management.models import Section, HomeWork, HomeWorkDocument, Exam, ExamDocument
import django_jalali.admin as jadmin # jalali date picker
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

    def get_readonly_fields(self, request, obj=None):
        # Check the model type and adjust readonly fields accordingly
        if obj and isinstance(obj, Student):  # Replace SomeModel with your actual model
            if request.user.is_superuser:
                return []  # Superusers can edit all fields
            if request.user.groups.filter(name="کارمند").exists():
                return ['first_name', 'phone']  # For Employees, field1 and field2 are readonly
            if request.user.groups.filter(name="استاد").exists():
                return ['last_name', 'code_melli']  # For Teachers, field3 and field4 are readonly
            
        
        # Default: make all fields editable

        return []  


    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_fieldsets(request, obj)  # Show all fields to superusers
        
        if obj and isinstance(obj, Student):
            
            if request.user.groups.filter(name="کارمند").exists():
                return (
                    (None, {
                        'fields': ('code_melli', 'grade', 'phone')  # Employees see these fields
                    }),
                )
            if request.user.groups.filter(name="استاد").exists():
                return (
                    (None, {
                        'fields': ('first_name', 'last_name')  # Teachers only see these fields
                    }),
                )


        return super().get_fieldsets(request, obj)





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

    # THIS IS WHAT TO APPLY TO ADD A JALALI DATE PICKER IN ADMIN PANEL
    formfield_overrides = {
        models.DateField: {'widget': jadmin.widgets.AdminjDateWidget},  # Use Jalali date picker in admin
    }


    inlines = [SectionStudentInline]


    