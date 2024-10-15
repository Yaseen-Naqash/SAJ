from django.db import models
import jdatetime
from a_user_management.models import Teacher, Student


# Create your models here.



class DaysOfWeek(models.TextChoices):
    SATURDAY = 'SAT', 'شنبه'
    SUNDAY = 'SUN', 'یکشنبه'
    MONDAY = 'MON', 'دوشنبه'
    TUESDAY = 'TUE', 'سه شنبه'
    WEDNESDAY = 'WED', 'چهارشنبه'
    THURSDAY = 'THU', 'پنجشنبه'
    FRIDAY = 'FRI', 'جمعه'


class Course(models.Model):

    INSTALLMENT = [
        ('0','ندارد'),
        ('1','دارد'),
    ]


    title = models.CharField(max_length=255, null=True, blank=True, verbose_name='نام دوره')
    description = models.TextField(max_length=2047, null=True , blank=True, verbose_name='توضیحات')
    prerequisites = models.ManyToManyField('Course', related_name='required_for',blank=True, verbose_name='پیشنیاز ها') # math101.required_for.all()  # Returns [math102]
    course_img = models.ImageField(upload_to='Course_images/', null=True, blank=True, verbose_name='تصویر دوره')
    price = models.CharField(max_length=127, null=True, blank=True, verbose_name='قیمت ثبت نام')
    installment = models.CharField(default=0,max_length=1,choices=INSTALLMENT, null=True, blank=True, verbose_name='اقساط')
    courseDuration = models.CharField(max_length=127, null=True , blank=True, verbose_name='مقدار جلسات دوره')

    class Meta:
        verbose_name = "دوره"  # Singular name for admin
        verbose_name_plural = "دوره ها"  # Plural name for admin

    def __str__(self):
        return self.title
    
class Section(models.Model):


    TYPE = [
        ('0','اتمام مهلت ثبت نام'),
        ('1','در حال ثبت نام'),
        
    ]

    name = models.CharField(max_length=63, null=True, blank=True, verbose_name='گروه') #or section number
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections', null=True, blank=True, verbose_name='دوره')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='sections', null=True, blank=True, verbose_name='استاد')
    students = models.ManyToManyField(Student, through='SectionStudent', related_name='sections', verbose_name='دانشجو ها')

    capacity = models.IntegerField(null=True, blank=True, default=1, verbose_name='ظرفیت')
    registered = models.IntegerField(null=True, blank=True, default=0, verbose_name='ثبت نام شده')
    section_status = models.CharField(default=1,max_length=1,choices=TYPE, verbose_name='وضعیت')
    session_number = models.IntegerField(null=True, blank=True, default=1, verbose_name=' تعداد جلسات برگزار شده ')

    class Meta:
        verbose_name = "سکشن" 
        verbose_name_plural = "سکشن ها" 

    def __str__(self):
        return f'{self.course.title} - {self.teacher} | {self.name}'
    
#  THIS IS A INTERMEDIATE CLASS FOR SHOWING STUDENT IN ADMIN PANEL OF SECTION, I COUDNT SHOW THEM DIRECTLY
#  I HAD TO USE  through='SectionStudent' AND THAT WAS ACHIVABLE WITH AN  Intermediary Model LIKE THIS
class SectionStudent(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_joined = models.DateField(auto_now_add=True)  # Additional fields

    def __str__(self):
        return f'{self.student}'
    
class SectionTimeSlot(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='time_slots')
    day_of_week = models.CharField(max_length=3, choices=DaysOfWeek.choices)  # Store the selected day
    timeOfSection = models.CharField(max_length=127, null=True, blank=True)
    place = models.CharField(max_length=63, null=True, blank=True)
    class Meta:
        unique_together = ('section', 'day_of_week')  # u cant have two time slot in same day
        verbose_name = "زمان سکشن" 
        verbose_name_plural = "زمان سکشن ها" 

    def __str__(self):
        return f"{self.section.course.title} | {self.section.teacher} | {self.section.name} | ({self.day_of_week} : {self.timeOfSection})"


class Attendance(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='attendances', null=True, blank=True, verbose_name='سکشن')
    section_student = models.ForeignKey(SectionStudent, on_delete=models.CASCADE, verbose_name='دانشجو')
    date = models.CharField(max_length=63, null=True, blank=True, verbose_name='تاریخ')  
    status = models.BooleanField(default=False, verbose_name='وضعیت')
    grg_date = models.DateField(auto_now_add=True, verbose_name='تاریخ')
    session = models.CharField(default='جلسه 1', max_length=31, null=True, blank=True, verbose_name='جلسه')

    class Meta:
        verbose_name = "حضور غیاب ها" 
        verbose_name_plural = "حضور غیاب" 


class Exam(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='exam', null=True, blank=True)
    exam_time = models.DateTimeField()

    class Meta:
        verbose_name = "آزمون" 
        verbose_name_plural = " آزمون ها" 
    
    def __str__(self):
        return f'آزمون برای {self.section.course.title} on {self.exam_time}'

class HomeWork(models.Model):
    title = models.CharField(max_length=127, null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='homeworks', null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='homeworks', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)  
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)      
    
    class Meta:
        verbose_name = "تمرین" 
        verbose_name_plural = "تمرین ها" 


    def __str__(self):
        return f' تمرین برای {self.section.course.title} توسط {self.teacher}'


class HomeWorkDocument(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='homeWorks', null=True, blank=True)
    homeWork = models.ForeignKey(HomeWork,on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    pdf = models.FileField(upload_to='homeWorks/pdfs/')  # 'documents/pdfs/' is the upload path
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "پاسخ تمرین" 
        verbose_name_plural = "پاسخ تمرین ها" 

    def __str__(self):
        return f' تمرین تحویلی از {self.student} برای {self.homeWork.section.teacher}'
    

class ExamDocument(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exams', null=True, blank=True)
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE, related_name='exams', null=True, blank=True)
    pdf = models.FileField(upload_to='homeWorks/pdfs/')  # 'documents/pdfs/' is the upload path
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = "پاسخ آزمون" 
        verbose_name_plural = "پاسخ آزمون ها" 

    
    def __str__(self):
        return f' ؛آزمون تحویلی از {self.student} برای {self.exam.section.teacher}'
    
class Degree(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='degrees', null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='degrees', null=True, blank=True)

    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = "مدرک" 
        verbose_name_plural = "مدارک" 

    def __str__(self):
        return f' مدرک : {self.course.title} برای {self.student}'