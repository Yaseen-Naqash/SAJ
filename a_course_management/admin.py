from django.utils import timezone
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib import admin
from .models import Course, Section, SectionStudent, SectionTimeSlot, Exam, HomeWork, HomeWorkDocument, ExamDocument, Degree, Attendance
from django_jalali.forms import jdatetime
import django_jalali.admin as jadmin # jalali date picker
from django.db import models  

from django.contrib import admin
from .models import Course, Section
from a_user_management.models import Student

# Register your models here.
admin.site.register(SectionTimeSlot)


class StudentInline(admin.TabularInline):
    model = Student
    extra = 1 

class SectionInline(admin.TabularInline):  
    model = Section
    extra = 1  

class SectionTimeSlotInline(admin.TabularInline):  
    model = SectionTimeSlot
    extra = 1  

class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 1
    can_delete = False
    fields = ('section_student', 'date', 'status')
    readonly_fields = ('section_student',)
    ordering = ['-date']

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


    def create_attendance(self, request, section_id, date=None):
        section = self.get_object(request, section_id)
        if not date:
            # Get the current Jalali date and set it using the custom field
            jalali_date = jdatetime.date.today()  # Get the current Jalali date
            date = jalali_date.strftime('%Y/%m/%d')
            

        session_value = f'جلسه {section.session_number}'
        for student in section.students.all():
            section_student = SectionStudent.objects.get(section=section, student=student)
            attendance, created = Attendance.objects.get_or_create(
                section=section,
                section_student=section_student,
                date=date,
                session=session_value,
                )
            
        if  created:
            section.session_number += 1  # Increment the session number by one
            section.save()  # Save the updated section
        messages.success(request, f' سند حضور غیاب برای {section} در تاریخ {date} ایجاد شد.')
        return redirect(f'/admin/a_course_management/section/{section_id}/change/')
    
    # Custom admin action to mark attendance for today
    def mark_attendance_today(self, request, queryset):
        for section in queryset:
            self.create_attendance(request, section.id)
        return redirect('/admin/a_course_management/attendance/')
    mark_attendance_today.short_description = 'ثبت حضور غیاب برای این سکشن'

    # Add a custom action in the admin panel
    actions = ['mark_attendance_today']



    search_fields = [
        'teacher__first_name', 
        'teacher__last_name',
        'course__title',
    ]
    list_filter = (
        'section_status',
        'course',
        'name',
    )


    inlines = [SectionTimeSlotInline]

@admin.register(SectionStudent)
class SectionStudentAdmin(admin.ModelAdmin):
    

    
    list_display= [
        'student',
        'section',
        'activity',
        'class_score',
        'exam_score',
    ]
    search_fields = [
        'student__first_name', 
        'student__last_name',
        'section__name',
        'section__teacher__first_name',
        'section__teacher__last_name',
    ]

    list_filter = (
        'activity',
        'section__course',
        'section',
    )

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [SectionInline]

@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    pass

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.DateTimeField: {'widget': jadmin.widgets.AdminSplitjDateTime},  # Use Jalali date picker in admin
    }

@admin.register(ExamDocument)
class ExamDocumentAdmin(admin.ModelAdmin):
    pass




@admin.register(HomeWork)
class HomeWorkAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.DateTimeField: {'widget': jadmin.widgets.AdminSplitjDateTime},  # Use Jalali date picker in admin
    }

@admin.register(HomeWorkDocument)
class HomeWorkDocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('section_student__student','section' , 'date', 'status', 'session')

    #   THIS PART HANDLED VIA get_list_filter METHOD BELOW
    #   list_filter = ('section_student__section', 'grg_date', 'session', 'section')

    search_fields = (
        'section_student__student__first_name',  # Accessing first_name through student
        'section_student__student__last_name',   # Accessing last_name through student
        'date',                                   # Date field in Attendance
    )
    actions = ['mark_attendance_present']


    # THIS METHOD LIMITS THE QS TO THE TEACHER SECTIONS
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='استاد').exists():
            return qs.filter(section__teacher=request.user.teacher)
        return qs
    

    # THIS METHOD LIMITS THE FILTER OPTIONS TO ONLY SHOW OBJECTS IN QS
    def get_list_filter(self, request):
        # Override the list_filter to only include options from the filtered queryset
        qs = self.get_queryset(request)

        # Get distinct values for each filter based on the queryset
        sections = qs.values_list('section', flat=True).distinct()
        grg_dates = qs.values_list('grg_date', flat=True).distinct()
        sessions = qs.values_list('session', flat=True).distinct()

        # Create custom filters for the available objects in the queryset
        return [
            ('section_student__section', admin.RelatedOnlyFieldListFilter),
            ('grg_date'),
            ('session', admin.AllValuesFieldListFilter),
            ('section', admin.RelatedOnlyFieldListFilter),
        ]
    
    # THIS METHOD SUBMITS attendance FOR SELECTED STUDENTS
    def mark_attendance_present(self, request, queryset):
        updated = queryset.update(status=True)
        self.message_user(request, f'حضور برای دانشجو های انتخاب شده ثبت شد ')
    
    mark_attendance_present.short_description = 'ثبت حضور'


