from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

from django.contrib import admin
from .models import Course, Section, SectionTimeSlot, Exam, HomeWork, HomeWorkDocument, ExamDocument, Degree
from a_user_management.admin import CustomAdminMixin
# Register your models here.
admin.site.register(SectionTimeSlot)

from django.contrib import admin
from .models import Course, Section

from a_user_management.models import Student

class StudentInline(admin.TabularInline):
    model = Student
    extra = 1 

class SectionInline(admin.TabularInline):  
    model = Section
    extra = 1  

class SectionTimeSlotInline(admin.TabularInline):  
    model = SectionTimeSlot
    extra = 1  

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display= [
        'course',
        'name',
        'teacher',
        'section_status',
        'capacity',
        'registered',


    ]
    readonly_fields = ['display_students']  # Add this to display students in the detail view
    # Method to display the list of students with links in the section edit view
    def display_students(self, obj):
        students = obj.students.all()  # Get all students in the section
        if students:
            # Generate a list of clickable links for each student
            return mark_safe(
                '<br>'.join([
                    format_html('<a href="{}"> {} </a>', 
                                reverse('admin:a_user_management_student_change', args=[student.pk]), 
                                student.get_full_name(),
                                )
                    for student in students
                ])
            )
        else:
            return "این گروه دانشجویی ندارد"

    display_students.short_description = "دانشجو های این گروه"

    # Optional: You can also keep it in the list_display if you want it on the list view as well
    def list_students(self, obj):
        return self.display_students(obj)  # Reuse the same method for the list view



    search_fields = [
        'name', 
        'teacher',
    ]
    list_filter = (
        'section_status',
        'course',
    )


    inlines = [SectionTimeSlotInline]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [SectionInline]




@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    pass

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    pass

@admin.register(ExamDocument)
class ExamDocumentAdmin(admin.ModelAdmin):
    pass




# TESTING GROUPS LIMITATIONS WITH CustomAdminMixin
@admin.register(HomeWork)
class HomeWorkAdmin(CustomAdminMixin, admin.ModelAdmin):
    # Any additional configurations for HomeWorkAdmin
    pass

@admin.register(HomeWorkDocument)
class HomeWorkDocumentAdmin(CustomAdminMixin, admin.ModelAdmin):
    pass


