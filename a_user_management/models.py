from django.contrib.auth.models import AbstractUser
from django.db import models
from a_institution_management.models import Branch, Institution

# Create your models here.



class Person(AbstractUser):
    code_melli = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, unique=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)       # Automatically updated on every save
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

class Owner(Person):
    institution = models.OneToOneField(Institution, on_delete=models.CASCADE, related_name='owner', null=True, blank=True)

    def __str__(self):
        return f"Owner: {self.first_name} {self.last_name}"
    
    


class Admin(Person): 
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='admins', null=True, blank=True)
    branch = models.OneToOneField(Branch, on_delete=models.CASCADE, related_name='admin', null=True, blank=True)

    def __str__(self):
        return f"Admin: {self.first_name} {self.last_name}"
    


class Employee(Person):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='employees', null=True, blank=True)    
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='employees', null=True, blank=True)

    def __str__(self):
        return f"Employee: {self.first_name} {self.last_name}"
    

class Teacher(Person):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='teachers', null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='teachers', null=True, blank=True)



    class Meta:
        verbose_name = "Teacher"  # Singular name for admin
        verbose_name_plural = "Teachers"  # Plural name for admin
    def __str__(self):
        return f"Teacher: {self.first_name} {self.last_name}"
    



class Grade(models.Model):
    title = models.CharField(max_length=127, null=True, blank=True)
    
    def __str__(self):
        return f'grade : {self.title}'

class Student(Person):
    ACTIVITY = [
        ('0','active'),
        ('1','ghost'),
    ]
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='students', null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='students', null=True, blank=True)
    grade = models.ForeignKey(Grade,on_delete=models.CASCADE, related_name='students', null=True, blank=True)
    activity = models.CharField(default=0,max_length=1,choices=ACTIVITY)

    # USERNAME_FIELD = 'phone'  # Use phone as the username


    class Meta:
        verbose_name = "Student"  # Singular name for admin
        verbose_name_plural = "Students"  # Plural name for admin
    def __str__(self):
        return f"Student: {self.first_name} {self.last_name}"