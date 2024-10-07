from django.db import models
from a_user_management.models import Teacher, Student

# Create your models here.

class DaysOfWeek(models.TextChoices):
    SATURDAY = 'SAT', 'Saturday'
    SUNDAY = 'SUN', 'Sunday'
    MONDAY = 'MON', 'Monday'
    TUESDAY = 'TUE', 'Tuesday'
    WEDNESDAY = 'WED', 'Wednesday'
    THURSDAY = 'THU', 'Thursday'
    FRIDAY = 'FRI', 'Friday'


class Course(models.Model):
    TYPE = [
        ('0','اتمام مهلت ثبت نام'),
        ('1','در حال ثبت نام'),
        
    ]
    INSTALLMENT = [
        ('0','ندارد'),
        ('1','دارد'),
    ]


    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=2047, null=True , blank=True)
    prerequisites = models.ManyToManyField('Course', related_name='required_for',blank=True) # math101.required_for.all()  # Returns [math102]
    course_img = models.ImageField(upload_to='Course_images/', null=True, blank=True)
    course_status = models.CharField(default=1,max_length=1,choices=TYPE)
    price = models.CharField(max_length=127, null=True, blank=True)
    installment = models.CharField(default=0,max_length=1,choices=INSTALLMENT, null=True, blank=True)
    courseDuration = models.CharField(max_length=127, null=True , blank=True)

    def __str__(self):
        return self.title
    
class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections', null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='sections', null=True, blank=True)
    students = models.ManyToManyField(Student, related_name='sections', blank=True)
    capacity = models.IntegerField(null=True, blank=True, default=1)
    registered = models.IntegerField(null=True, blank=True, default=0)
    

    def __str__(self):
        return f'{self.course.title} - {self.teacher}'
class SectionTimeSlot(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='time_slots')
    day_of_week = models.CharField(max_length=3, choices=DaysOfWeek.choices)  # Store the selected day
    timeOfSection = models.CharField(max_length=127, null=True, blank=True)
    place = models.CharField(max_length=63, null=True, blank=True)
    class Meta:
        unique_together = ('section', 'day_of_week')  # u cant have two time slot in same day

    def __str__(self):
        return f"{self.section} ({self.day_of_week} : {self.timeOfSection})"


class Exam(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='exams', null=True, blank=True)
    exam_time = models.DateTimeField()  # Date and time of the exam
    duration = models.DurationField()   # Exam duration (optional)

    def __str__(self):
        return f'Exam for {self.course.title} on {self.exam_time}'

class HomeWork(models.Model):
    title = models.CharField(max_length=127, null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='homeworks', null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='homeworks', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)       # Automatically updated on every save
    
    def __str__(self):
        return f'HomeWork for {self.course} by {self.teacher}'


class HomeWorkDocument(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='homeWorks', null=True, blank=True)
    homeWork = models.ForeignKey(HomeWork,on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    pdf = models.FileField(upload_to='homeWorks/pdfs/')  # 'documents/pdfs/' is the upload path
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)  
    def __str__(self):
        return self.student