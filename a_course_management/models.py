from django.db import models
import jdatetime # type: ignore
from a_user_management.models import Teacher, Student
from decimal import Decimal

from django.core.exceptions import ValidationError
# Create your models here.





class Course(models.Model):

    INSTALLMENT = [
        ('0','ندارد'),
        ('1','دارد'),
    ]


    title = models.CharField(max_length=255, null=True, verbose_name='نام دوره')
    prerequisites = models.ManyToManyField('Course', related_name='required_for',blank=True, verbose_name='پیشنیاز ها') # math101.required_for.all()  # Returns [math102]
    course_img = models.ImageField(upload_to='Course_images/', null=True, verbose_name='تصویر دوره')
    price = models.CharField(max_length=127, null=True, verbose_name='قیمت ثبت نام به تومان')
    installment = models.CharField(default=0,max_length=1,choices=INSTALLMENT, null=True, blank=True, verbose_name='اقساط')
    courseDuration = models.CharField(max_length=63, null=True , blank=True, verbose_name='تعداد جلسات دوره')
    session_length = models.CharField(max_length=63, null=True , blank=True, verbose_name='مدت زمان هر جلسه')
    course_hours = models.IntegerField(default=10, null=True, verbose_name='تعداد ساعت دوره')
    description = models.TextField(max_length=2047, null=True , blank=True, verbose_name='توضیحات')
    
    class Meta:
        verbose_name = "دوره"  # Singular name for admin
        verbose_name_plural = "2- دوره ها"  # Plural name for admin

    def __str__(self):
        return self.title
    
class Section(models.Model):


    TYPE = [
        ('0','اتمام مهلت ثبت نام'),
        ('1','در حال ثبت نام'),
        
    ]

    GENDER = [
        ('0','دخنر'),
        ('1','پسر'),
        ('2','مختلط'),
    ]

    name = models.CharField(max_length=63, null=True, blank=True, verbose_name='گروه') #or section number
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, related_name='sections', null=True, blank=True, verbose_name='دوره')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, related_name='sections', null=True, blank=True, verbose_name='استاد')
    students = models.ManyToManyField(Student, through='SectionStudent', related_name='sections', verbose_name='دانشجو ها')
    online_section = models.BooleanField(default=False, verbose_name='برگزاری آنلاین')
    capacity = models.IntegerField(null=True, blank=True, default=1, verbose_name='ظرفیت')
    section_status = models.CharField(default=1,max_length=1,choices=TYPE, verbose_name='وضعیت')
    session_number = models.IntegerField(null=True, blank=True, default=0, verbose_name=' تعداد جلسات برگزار شده ')
    gender = models.CharField(max_length=1, null=True, blank=True, choices=GENDER, verbose_name="جنسیت")


    @property
    def registered(self):
        return self.students.count()

    class Meta:
        verbose_name = "گروه"
        verbose_name_plural = "3- گروه ها" 

    def __str__(self):
        return f'{self.course.title} - {self.teacher} | {self.name}'
    
#  THIS IS A INTERMEDIATE CLASS FOR SHOWING STUDENT IN ADMIN PANEL OF SECTION, I COUDNT SHOW THEM DIRECTLY
#  I HAD TO USE  through='SectionStudent' AND THAT WAS ACHIVABLE WITH AN  Intermediary Model LIKE THIS
#  IT ALSO REPERESENT STUDENT IN SECTION LINK THAT CONTAINS SOME INFORMATION UNIQUE TO STUDENT AND SECTION 
#  THAT HES BELONG TO LIKE HIS SCORE IN THAT SECTION

class SectionStudent(models.Model):

    ACTIVITY = [
        ('0','در حال تحصیل'),
        ('1','دوره پایان یافته | قبول'),
        ('2','دوره پایان یافته | مردود'),

    ]

    section = models.ForeignKey(Section, on_delete=models.SET_NULL, verbose_name='گروه', null=True)
    student = models.ForeignKey(Student, related_name='section_student', on_delete=models.SET_NULL, verbose_name='دانشجو', null=True)
    activity = models.CharField(default=0,max_length=1,choices=ACTIVITY, verbose_name="وضعیت دانشجو در این دوره")

    date_joined = models.DateField(auto_now_add=True)  # Additional fields
    class_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='نمره کلاسی')
    exam_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='نمره پایانی')
    start_date = models.DateField(verbose_name='تاریخ شروع', null=True, blank=True)
    end_date = models.DateField(verbose_name='تاریخ پایان', null=True, blank=True)
    # you ask question about when this date should register


    @property
    def score(self):
        if self.class_score and self.exam_score:
            score = (Decimal('0.7') * self.class_score) + (Decimal('0.3') * self.exam_score)
            return (f'{score}')
        return "بدون نمره"

    class Meta:
        verbose_name = "دوره برای دانشجو" 
        verbose_name_plural = "1- اطلاعات تحصیلی" 


    def clean(self):
        """
        Custom validation to ensure only one active student in the same section.
        """
        if self.activity == '0':
            # Check for existing '0' activity for the same student in the same section
            existing = SectionStudent.objects.filter(
                section=self.section, 
                student=self.student, 
                activity='0'
            ).exclude(id=self.id)  # Exclude the current instance if editing
            if existing.exists():
                raise ValidationError("این دانشجو در این گروه هم‌اکنون با وضعیت 'در حال تحصیل' ثبت شده است.")

    def save(self, *args, **kwargs):
        """
        Override save to ensure `clean` is called.
        """
        self.full_clean()  # Ensures `clean` is called before saving
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.student} در {self.section}'
    
class SectionTimeSlot(models.Model):

    DAYS_OF_WEEK = [
        ('0','شنبه'),
        ('1','یکشنبه'),
        ('2','دوشنبه'),
        ('3','سه شنبه'),
        ('4','چهارشنبه'),
        ('5','پنجشنبه'),
        ('6','جمعه'),
        
    ]


    section = models.ForeignKey(Section, on_delete=models.SET_NULL, related_name='time_slots', verbose_name='گروه', null=True)
    day_of_week = models.CharField(max_length=1, choices=DAYS_OF_WEEK, verbose_name='روز')  # Store the selected day
    timeOfSection = models.CharField(max_length=127, null=True, verbose_name='زمان')
    place = models.CharField(max_length=63, null=True, verbose_name='مکان')
    class Meta:
        verbose_name = "زمان سکشن"
        verbose_name_plural = "زمان سکشن ها" 

    def __str__(self):
        return f"{self.section.course.title} | {self.section.teacher} | {self.section.name} | ({self.day_of_week} : {self.timeOfSection})"

    
class Attendance(models.Model):
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, related_name='attendances', null=True, blank=True, verbose_name='سکشن')
    section_student = models.ForeignKey(SectionStudent,related_name='attendances', on_delete=models.SET_NULL, verbose_name='دانشجو', null=True)
    date = models.CharField(max_length=63, null=True, blank=True, verbose_name='تاریخ')  
    status = models.BooleanField(default=False, verbose_name='وضعیت')
    grg_date = models.DateField(auto_now_add=True, verbose_name='تاریخ')
    session = models.CharField(default='جلسه 1', max_length=31, null=True, blank=True, verbose_name='جلسه')

    class Meta:
        verbose_name = "حضور غیاب ها" 
        verbose_name_plural = "4- حضور غیاب" 


class Exam(models.Model):
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, related_name='exam', null=True, blank=True, verbose_name='گروه')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, related_name='exams', null=True, blank=True, verbose_name='استاد')

    exam_time = models.DateTimeField(verbose_name='تاریخ آزمون')

    class Meta:
        verbose_name = "آزمون" 
        verbose_name_plural = "8- آزمون ها" 
    
    def __str__(self):
        return f'آزمون برای {self.section.course.title} | {self.teacher} | {self.section.name}'

class HomeWork(models.Model):
    title = models.CharField(max_length=127, null=True, blank=True, verbose_name='عنوان')
    pdf = models.FileField(upload_to='GivenHomeWorks/files/', verbose_name='فایل پیوست', null=True , blank=True)  # 'documents/pdfs/' is the upload path
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, related_name='homeworks', null=True, blank=True, verbose_name='گروه')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, related_name='homeworks', null=True, blank=True, verbose_name='استاد')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)  
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    expire_time = models.DateTimeField(verbose_name='مهلت تحویل')
    description = models.TextField(max_length=2047, null=True , blank=True, verbose_name='توضیحات')

    
    class Meta:
        verbose_name = "تمرین" 
        verbose_name_plural = "6- تمرین ها" 


    def __str__(self):
        return f' تمرین برای {self.section.course.title} توسط {self.teacher}'


class HomeWorkDocument(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, related_name='homeWorks', null=True, blank=True, verbose_name='دانش آموزش')
    homeWork = models.ForeignKey(HomeWork,on_delete=models.SET_NULL, related_name='documents', null=True, blank=True, verbose_name='تمرین')
    pdf = models.FileField(upload_to='HomeWorks/files/')  # 'documents/pdfs/' is the upload path
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    seen = models.BooleanField(default=False, verbose_name='وضعیت')
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='نمره')

    
    class Meta:
        verbose_name = "پاسخ تمرین" 
        verbose_name_plural = "7- پاسخ تمرین ها" 

    def __str__(self):
        return f' تمرین تحویلی از {self.student} برای {self.homeWork.section.teacher}'
    
class ExamDocument(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, related_name='exams', null=True, blank=True)
    exam = models.ForeignKey(Exam,on_delete=models.SET_NULL, related_name='exams', null=True, blank=True)
    pdf = models.FileField(upload_to='homeWorks/pdfs/')  # 'documents/pdfs/' is the upload path
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = "پاسخ آزمون" 
        verbose_name_plural = "9- پاسخ آزمون ها" 

    
    def __str__(self):
        return f' ؛آزمون تحویلی از {self.student} برای {self.exam.section.teacher}'
    
class Degree(models.Model):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, related_name='degrees', null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, related_name='degrees', null=True, blank=True)
    pdf = models.FileField(upload_to='Degrees/', verbose_name='فایل پیوست مدرک', null=True , blank=True)  # 'documents/pdfs/' is the upload path
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    course_hours = models.IntegerField(default=10, null=True, verbose_name='تعداد ساعت دوره')
    serial = models.CharField(max_length=127, null=True, verbose_name='شماره سریال')
    j_create_date = models.CharField(max_length=15, default=jdatetime.date.today().strftime('%Y/%m/%d'), verbose_name='تاریخ صدور')

    class Meta:
        verbose_name = "مدرک"
        verbose_name_plural = "5- مدارک"
        unique_together = ('course', 'student')


    def __str__(self):
        return f' مدرک : {self.course.title} برای {self.student}'