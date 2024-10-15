from django.utils import timezone
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib import admin
from .models import Course, Section, SectionStudent, SectionTimeSlot, Exam, HomeWork, HomeWorkDocument, ExamDocument, Degree, Attendance
from a_user_management.admin import CustomAdminMixin
from django_jalali.forms import jdatetime, jDateInput



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


class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 1
    can_delete = False
    fields = ('section_student', 'date', 'status')
    readonly_fields = ('section_student',)
    ordering = ['-date']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Only display records for the current section
        return qs.filter(section_student__section__teacher=request.user.teacher)

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Teacher').exists():
            return qs.filter(teacher=request.user.teacher)
        return qs
    
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


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('section_student', 'date', 'status', 'session')
    list_filter = ('section_student__section', 'grg_date', 'session', 'section')
    search_fields = (
        'section_student__student__first_name',  # Accessing first_name through student
        'section_student__student__last_name',   # Accessing last_name through student
        'date',                                   # Date field in Attendance
    )
    actions = ['mark_attendance_present']


    # Define the custom action
    def mark_attendance_present(self, request, queryset):
        updated = queryset.update(status=True)
        self.message_user(request, f'حضور برای دانشجو های انتخاب شده ثبت شد ')
    
    mark_attendance_present.short_description = 'ثبت حضور'


