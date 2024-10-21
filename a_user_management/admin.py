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






#STUDENT
@admin.register(Student)
class StudentAdmin(AdminPermissionMixin, admin.ModelAdmin):

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


    