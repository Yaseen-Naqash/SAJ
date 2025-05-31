from django.forms import ValidationError
from django.utils import timezone
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib import admin
from .models import Course, Section, SectionStudent, SectionTimeSlot, Exam, HomeWork, HomeWorkDocument, ExamDocument, Degree, Attendance
from a_user_management.admin import TeacherFilter
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
from SAJ.custom_permissions import AdminPermissionMixin
from django.contrib.humanize.templatetags.humanize import intcomma
from django.template.defaultfilters import timesince


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

from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse
from django import forms
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect

class SectionStudentScoreForm(forms.ModelForm):
    class Meta:
        model = SectionStudent
        fields = ['class_score', 'exam_score']

    

SectionStudentScoreFormSet = modelformset_factory(
    SectionStudent,
    form=SectionStudentScoreForm,
    extra=0,  # No extra forms
)

@admin.register(Section)
class SectionAdmin(AdminPermissionMixin, admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('create-attendance/<int:section_id>/', self.admin_site.admin_view(self.create_attendance), name='create-attendance'),
            path('enter-scores/<int:section_id>/', self.admin_site.admin_view(self.enter_scores_view), name='enter_scores'),
            path('end_section/<int:section_id>/', self.admin_site.admin_view(self.end_section_view), name='end_section'),
        ]
        return custom_urls + urls
    
    list_display= [
        'course',
        'name',
        'teacher',
        'method',
        # 'section_status',
        'capacity',
        'registered_count',
        'students_data',
        'enter_scores_button',
        'end_section_button',
        'attendance_button',
        
    ]
    def enter_scores_view(self, request, section_id):
        section = get_object_or_404(Section, pk=section_id)
        # Filter for active students only (or adjust as needed)
        queryset = section.section_students.filter(activity='0')
        formset = SectionStudentScoreFormSet(queryset=queryset)
        if request.method == "POST":
            formset = SectionStudentScoreFormSet(request.POST, queryset=queryset)
            if formset.is_valid():
                formset.save()
                self.message_user(request, "نمرات با موفقیت به‌روزرسانی شدند.", messages.SUCCESS)
                # Redirect back to the section change page
                return redirect('admin:a_course_management_section_changelist')
            else:
                self.message_user(request, f"خطا در به‌روزرسانی نمرات: {formset.errors}", messages.ERROR)

        context = {
            **self.admin_site.each_context(request),
            'formset': formset,
            'section': section,
            'opts': self.model._meta,
            
        }
        return TemplateResponse(request, "admin/enter_scores.html", context)

    def enter_scores_button(self, obj):
        url = reverse('admin:enter_scores', args=[obj.id])
        return format_html('<a class="button" href="{}">ثبت نمرات</a>', url)
    enter_scores_button.short_description = "ثبت نمرات"
    def get_list_display(self, request):
        """
        Modify the list_display to conditionally hide 'end_section_button' 
        based on whether the user is in the 'استاد' group.
        """
        list_display = super().get_list_display(request)
        
        if request.user.groups.filter(name='استاد').exists():

            # Remove 'end_section_button' from list_display if the user is not in 'استاد' group
            list_display = [field for field in list_display if field != 'end_section_button']
        
        return list_display

    
    def registered_count(self, obj):
        if obj.registered > obj.capacity:
            color = 'red'
        elif obj.registered == obj.capacity:
            color = 'yellow'
        else:
            color = 'green'
        # Return the value wrapped in styled HTML
        return format_html(
            '<span style="color: {};">{}</span>', color, obj.registered
        )    
    registered_count.short_description = "ثبت نام شده"

    
    def end_section_button(self, obj):
        url = reverse('admin:end_section', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" onclick="return confirm(\'آیا برای اتمام این دوره و صدور مدرک مطمن هستید؟\')">اتمام دوره</a>',
            url,
        )
    end_section_button.short_description = "اتمام دوره"

    def students_data(self, obj):
        # Construct the URL dynamically
        url = reverse('admin:a_course_management_sectionstudent_changelist')
        query_params = f"activity__exact=0&section__id__exact={obj.id}"
        full_url = f"{url}?{query_params}"
        return format_html('<a href="{}">مشاهده</a>', full_url)
    students_data.short_description = "دانشجو ها"


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
        students = Student.objects.filter(section_students__section=obj, section_students__activity='0')
        # students = obj.students.all()  # Get all students in the section

        if students:
                        # Create table header
            table_html = """
                <table class="table table-striped table-bordered">
                    <thead>
                        <tr>
                            <th>شماره</th>
                            <th>نام دانشجو</th>
                            <th>آخرین قسط پرداختی</th>
                            <th>بدهی</th>
                            <th>جزئیات بیشتر</th>
                        </tr>
                    </thead>
                    <tbody>
            """

            # Populate table rows
            for index, student in enumerate(students, start=1):
                latest_receipt = student.receipts.filter(section=obj).order_by('-created_at').first()  # Fetch the latest receipt by created_at

                if latest_receipt:
                    # Calculate the time passed since the latest receipt was created
                    time_since = timesince(latest_receipt.created_at)
                else:
                    time_since = "ندارد"  # If no receipts, display "ندارد"


                debt = student.balance  # Assuming a method to calculate debt
                
                # Format debt with commas
                formatted_debt = "{:,}".format(int(debt))

                # Determine color based on debt sign
                if debt > 0:
                    debt_html = format_html('<span style="color: green;">{}</span>', formatted_debt)
                elif debt < 0:
                    debt_html = format_html('<span style="color: red;">{}</span>', formatted_debt.lstrip('-'))
                else:
                    debt_html = format_html('<span>{}</span>', formatted_debt)



                table_html += format_html(
                    """
                    <tr>
                        <td>{}</td>
                        <td><a href="{}">{}</a></td>
                        <td>{}</td>
                        <td>{}</td>
                        <td><a href="{}" class="button">مشاهده جزئیات</a></td>
                    </tr>
                    """,
                    index,
                    reverse('admin:a_user_management_student_change', args=[student.pk]),
                    student.get_full_name(),
                    time_since,
                    debt_html,
                    reverse('admin:a_financial_management_receipt_changelist') + f'?payer__id__exact={student.id}'  # Link to a detailed view
                ) 

            # Close table
            table_html += "</tbody></table>"

            return mark_safe(table_html)
        else:
            return "این گروه دانشجویی ندارد"

    display_students.short_description = "دانشجو های در حال تحصیل این گروه"

    

    # Optional: You can also keep it in the list_display if you want it on the list view as well
    def list_students(self, obj):
        return self.display_students(obj)  # Reuse the same method for the list view



    




    
    def attendance_button(self, obj):
        create_attendance_url = reverse('admin:create-attendance', kwargs={'section_id': obj.id})  
        date = jdatetime.date.today().strftime('%Y/%m/%d')  # Current Jalali date
        session = f'جلسه {obj.session_number+1}'

        return format_html(
            '<a class="button" href="{}" onclick="return confirm(\'آیا برای ثبت حضور غیاب این گروه در تاریخ {} و {} مطمئن هستید؟\')">'
            'ثبت حضوروغیاب</a>',
            create_attendance_url, date, session
        )

    attendance_button.short_description = "ثبت حضوروغیاب"

    def create_attendance(self, request, section_id):
        section = Section.objects.get(id=section_id)
        date = jdatetime.date.today().strftime('%Y/%m/%d')  # Current Jalali date
        session_value = f'جلسه {section.session_number + 1}'

        for student in section.students.all():
            section_student = SectionStudent.objects.get(section=section, student=student)
            attendance, created = Attendance.objects.get_or_create(
                section=section,
                section_student=section_student,
                date=date,
                session=session_value,
            )

        if created:
            section.session_number += 1  # Increment session number
            section.save()

        messages.success(request, f'سند حضور غیاب برای {section} در تاریخ {date} ایجاد شد.')

        # Redirect to the attendance admin page with the proper filter
        return redirect(f'/admin/a_course_management/attendance/?section__id__exact={section.id}&session={session_value}')


    search_fields = [
        'teacher__first_name', 
        'teacher__last_name',
        'course__title',
        'name',
    ]
    list_filter = (
        'section_status',
        TeacherFilter,
    )


    inlines = [SectionStudentInline, SectionTimeSlotInline, ]
    
    def save_formset(self, request, form, formset, change):
        try:
            super().save_formset(request, form, formset, change)
        except ValidationError as e:
            # Extract and clean up the error message
            error_messages = e.message_dict.get('__all__', e.messages)  # Get messages under '__all__'
            clean_message = " ".join(error_messages)  # Join messages into a single string
            clean_message = clean_message.replace('\u200c', '')  # Remove zero-width spaces
            self.message_user(request, f"دانشجو اضافه نشد: {clean_message}", level='error')
    formfield_overrides = {
        models.DateField: {'widget': jadmin.widgets.AdminjDateWidget},  # Use Jalali date picker in admin
    }



# Define a custom filter for the course
class CourseFilter(admin.SimpleListFilter):
    title = ('دوره')  # The title of the filter
    parameter_name = 'section__course'

    def lookups(self, request, model_admin):
        if request.user.groups.filter(name='استاد').exists():
            # If the user is a teacher, show only courses associated with them
            return [(section.course.id, section) for section in Section.objects.filter(teacher=request.user)]
        else:
            # If the user is not a teacher, show all courses
            return [(section.course.id, section) for section in Section.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(section__course_id=self.value())
        return queryset

@admin.register(SectionStudent)
class SectionStudentAdmin(AdminPermissionMixin, admin.ModelAdmin):
    

    readonly_fields = ('get_score',)

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
        CourseFilter,  # Add the custom course filter
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

    def get_actions(self, request):
        actions = super().get_actions(request)
        # Check if the user belongs to the 'استاد' group
        allowed_groups = ['کارمند', 'مدیر']
        if not request.user.groups.filter(name__in=allowed_groups).exists():
            # Remove the 'end_section' action if the user is not in the 'استاد' group
            if 'end_section' in actions:
                del actions['end_section']
        return actions
    
    formfield_overrides = {
        models.DateField: {'widget': jadmin.widgets.AdminjDateWidget},  # Use Jalali date picker in admin
    }

    def get_score(self, obj):
        return obj.score  # Access the `score` property
    get_score.short_description = 'نمره کل' 

@admin.register(Course)
class CourseAdmin(AdminPermissionMixin, admin.ModelAdmin):

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
    autocomplete_fields = ('student',)


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.DateTimeField: {'widget': jadmin.widgets.AdminSplitjDateTime},  # Use Jalali date picker in admin
    }

@admin.register(ExamDocument)
class ExamDocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(HomeWork)
class HomeWorkAdmin(AdminPermissionMixin, admin.ModelAdmin):
    formfield_overrides = {
        models.DateTimeField: {'widget': jadmin.widgets.AdminSplitjDateTime},  # Use Jalali date picker in admin
    }

@admin.register(HomeWorkDocument)
class HomeWorkDocumentAdmin(AdminPermissionMixin, admin.ModelAdmin):
    
    
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
        'seen',
    )


@admin.register(Attendance)
class AttendanceAdmin(AdminPermissionMixin, admin.ModelAdmin):
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





