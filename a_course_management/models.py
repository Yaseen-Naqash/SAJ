from django.db import models
from a_user_management.models import Teacher, Student

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=255, null=True)
    description = models.TextField(max_length=2047, null=True)
    students = models.ManyToManyField(Student, related_name='courses')
    teachers = models.ManyToManyField(Teacher, related_name='courses')
    prerequisites = models.ManyToManyField('Course', related_name='required_for') # math101.required_for.all()  # Returns [math102]
    course_img = models.ImageField(upload_to='Course_images/', null=True, blank=True)


    def __str__(self):
        return self.title
    
class ClassSession(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='class_sessions')
    start_time = models.DateTimeField()  # Start date and time of the class
    end_time = models.DateTimeField()    # End date and time of the class

    def __str__(self):
        return f'{self.course.title} - {self.start_time}'

class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    exam_time = models.DateTimeField()  # Date and time of the exam
    duration = models.DurationField()   # Exam duration (optional)

    def __str__(self):
        return f'Exam for {self.course.title} on {self.exam_time}'

class HomeWork(models.Model):
    title = models.CharField(max_length=127, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='homeworks')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='homeworks')
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)       # Automatically updated on every save
    
    def __str__(self):
        return f'HomeWork for {self.course} by {self.teacher}'


class HomeWorkDocument(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='homeWorks')
    homeWork = models.ForeignKey(HomeWork,on_delete=models.CASCADE, related_name='documents')
    pdf = models.FileField(upload_to='homeWorks/pdfs/')  # 'documents/pdfs/' is the upload path
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)  
    def __str__(self):
        return self.student