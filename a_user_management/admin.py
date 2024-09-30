from django.contrib import admin
from .models import Student, Teacher, Person
# Register your models here.



admin.site.register(Person)
admin.site.register(Student)
admin.site.register(Teacher)