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
from django.templatetags.static import static
from django.contrib import admin
from .models import Course, Section
from a_user_management.models import Student
from decimal import Decimal
from django.urls import path
from django.shortcuts import redirect




def process_section_students(request, queryset):
    # Check for students with missing scores
    missing_scores = queryset.filter(class_score__isnull=True) | queryset.filter(exam_score__isnull=True)
    missing_count = missing_scores.count()

    if missing_count > 0:
        # If there are students with missing scores, show an error message
        return f"{missing_count} دانشجو نمره ثبت نشده دارند", False

    # Process each SectionStudent to create Degree objects and update activity
    created_degrees = 0
    for section_student in queryset:
        # Calculate the score
        score = (Decimal('0.7') * section_student.class_score) + (Decimal('0.3') * section_student.exam_score)
        if score >= 70:
            # Create the Degree object
            Degree.objects.create(
                course=section_student.section.course,
                student=section_student.student,
                score=score,
                course_hours=section_student.section.course.course_hours,
            )
            created_degrees += 1
            section_student.activity = '1'
        else:
            section_student.activity = '2'
        section_student.save()

    updated_count = queryset.count()
    return (
        f"دوره برای {updated_count} دانشجو به اتمام رسید. {created_degrees} دانشجو قبول و {updated_count - created_degrees} دانشجو مردود شدند. مدارک قبول شدگان در بخش مدارک قابل مشاهده است.",
        True,
    )


# Register your models here.
# admin.site.register(SectionTimeSlot)


class StudentInline(admin.TabularInline):
    model = Student
    extra = 0

class SectionInline(admin.TabularInline):  
    model = Section
    extra = 0

class SectionTimeSlotInline(admin.TabularInline):  
    model = SectionTimeSlot
    extra = 0

class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0
    can_delete = False
    fields = ('section_student', 'date', 'status')
    readonly_fields = ('section_student',)
    ordering = ['-date']

class SectionStudentInline(admin.TabularInline):
    model = SectionStudent
    extra = 1
    verbose_name = "دانشجو"
    verbose_name_plural = "دانشجو ها"
    fields = ('student',)

    autocomplete_fields = ['student']
    # Override the queryset to hide existing students in the inline
    def get_queryset(self, request):
        return SectionStudent.objects.none()


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):

    
    list_display= [
        'course',
        'name',
        'teacher',
        'section_status',
        'capacity',
        'registered',
        'end_section_button',
    ]

    
    def end_section_button(self, obj):
        url = reverse('admin:end_section', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" onclick="return confirm(\'آیا برای اتمام این دوره و صدور مدرک مطمن هستید؟\')">اتمام دوره</a>',
            url,
        )
    end_section_button.short_description = "اتمام دوره"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'end_section/<int:section_id>/',
                self.admin_site.admin_view(self.end_section_view),
                name='end_section',
            ),
        ]
        return custom_urls + urls

    def end_section_view(self, request, section_id):
        section = Section.objects.get(pk=section_id)
        section_students = SectionStudent.objects.filter(section=section)

        # Process the SectionStudent records
        message, success = process_section_students(request, section_students)

        if success:
            self.message_user(request, message, messages.SUCCESS)
        else:
            self.message_user(request, message, messages.ERROR)

        return redirect(f"{reverse('admin:a_course_management_section_changelist')}")

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
            

        session_value = f'جلسه {section.session_number+1}'
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
        'name',
    ]
    list_filter = (
        'section_status',
        'course',
    )


    inlines = [SectionStudentInline, SectionTimeSlotInline, ]
    formfield_overrides = {
        models.DateField: {'widget': jadmin.widgets.AdminjDateWidget},  # Use Jalali date picker in admin
    }


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

    # Define the action method
    def end_section(self, request, queryset):

                # Check for students with missing scores
        missing_scores = queryset.filter(class_score__isnull=True) | queryset.filter(exam_score__isnull=True)
        
        missing_count = missing_scores.count()

        # If there are students with missing scores, show an error message
        if missing_count > 0:
            self.message_user(
                request,
                f"{missing_count} دانشجو نمره ثبت نشده دارند",
                messages.ERROR
            )
        else:
            # Process each SectionStudent to create Degree objects and update activity
            created_degrees = 0
            for section_student in queryset:
                # Calculate the score

                score = (Decimal('0.7') * section_student.class_score) + (Decimal('0.3') * section_student.exam_score)
                if score >= 70:

                    # Create the Degree object
                    Degree.objects.create(
                        course=section_student.section.course,
                        student=section_student.student,
                        score=score,
                        course_hours=section_student.section.course.course_hours
                    )
                    created_degrees += 1
                    section_student.activity = '1'
                    section_student.save()
                else:
                    section_student.activity = '2'
                    section_student.save()
                
            
            updated_count = queryset.count()

            self.message_user(
                request,
                f"دوره برای {updated_count} دانشجو به اتمام رسید. {created_degrees} دانشجو قبول و {updated_count-created_degrees} دانشجو مردود شدند. مدارک قبول شدگان در بخش مدارک قابل مشاهده است.",
                messages.SUCCESS
            )

    # Register the action with a display name
    end_section.short_description = "اتمام دوره و صدور مدرک"

    # Add the action to the actions list
    actions = [end_section]

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display= [
        'title',
        'price',
        'installment',
        'courseDuration',
        'session_length',
    ]
    search_fields = [
        'title', 

    ]
    list_filter = (
        'installment',

    )

    class Media:
        js = ('/static/js/admin/admin_price_format.js',)
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        form_field = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'price':
            form_field.widget.attrs.update({'class': 'comma-add'})
        return form_field
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
    
    
    list_display= [
        'student',
        'homeWork',
        'get_section',

        'seen',
        'score',
    ]

    # Define a custom method to display the section with verbose name 'گروه'
    def get_section(self, obj):
        return obj.homeWork.section
    get_section.short_description = 'گروه'  # This sets the column label in the admin

    search_fields = [
        'student__first_name', 
        'student__last_name',
    ]

    list_filter = (
        'homeWork',
        'seen',
        'homeWork__section',
    )


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('get_students' ,'section' , 'date', 'status', 'session')

    def get_students(self, obj):
        return obj.section_student.student
    get_students.short_description = 'دانش آموز'  # This sets the column label in the admin


    #   THIS PART HANDLED VIA get_list_filter METHOD BELOW
    #   list_filter = ('section_student__section', 'grg_date', 'session', 'section')

    search_fields = (
        'section_student__student__first_name',  # Accessing first_name through student
        'section_student__student__last_name',   # Accessing last_name through student
        'date',                                   # Date field in Attendance
    )
    actions = ['mark_attendance_present']

    

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


