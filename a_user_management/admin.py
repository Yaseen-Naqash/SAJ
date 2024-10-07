from django.contrib import admin
from .models import Student, Teacher, Person, PhoneVerification
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin
from django.db import models  # This import was missing
# Register your models here.



class StudentAdmin(admin.ModelAdmin):
    list_filter = (
        ('last_login', JDateFieldListFilter),    
        ('date_joined', JDateFieldListFilter), 
        ('date_of_birth', JDateFieldListFilter),  
        
    )
    formfield_overrides = {
        models.DateField: {'widget': jadmin.widgets.AdminjDateWidget},  # Use Jalali date picker in admin
    }
    
admin.site.register(Person)
admin.site.register(Teacher)
admin.site.register(Student, StudentAdmin)
admin.site.register(PhoneVerification)
