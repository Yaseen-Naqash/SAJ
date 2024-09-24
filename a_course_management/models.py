from django.db import models
from a_user_management.models import Teacher

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=255, null=True)
    description = models.TextField(max_length=2047, null=True)

    teachers = models.ManyToManyField(Teacher, related_name='courses')
    prerequisites = models.ManyToManyField('Course', related_name='required_for') # math101.required_for.all()  # Returns [math102]



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
