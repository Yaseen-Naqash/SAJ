from django.contrib.auth.models import AbstractUser
from django.db import models
from a_institution_management.models import Branch, Institution
import random
from django.utils import timezone

class Person(AbstractUser):
    code_melli = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, unique=True, blank=True)
    phone2 = models.CharField(max_length=11, null=True, unique=True, blank=True)

    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)       # Automatically updated on every save
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    

class PhoneVerification(models.Model):
    phone_number = models.CharField(max_length=11,null=True, blank=True)  # Adjust length as necessary
    verification_code = models.CharField(max_length=4, null=True, blank=True)  # Assuming 4-digit code
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):

        return timezone.now() > self.created_at + timezone.timedelta(seconds=120)

    def generate_code(self):
        self.verification_code = str(random.randint(1000, 9999))



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
    EDUCATION = [
        ('0','ابتدایی'),
        ('1','متوسطه اول'),
        ('2','متوسطه دوم'),
        ('3','دیپلم'),
        ('4','کاردانی'),
        ('5','کارشناسی'),
        ('6','کارشناسی ارشد'),
        ('7','دکتری'),
    ]

    AGE_LEVEL = [
        ('0','کودک'),
        ('1','نوجوان'),
        ('2','بزرگسال'),
    ]

    PROGRAMING = [
        ('0','مبتدی'),
        ('1','تعین سطح'),
    ]
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='students', null=True, blank=True)
    grade = models.ForeignKey(Grade,on_delete=models.CASCADE, related_name='students', null=True, blank=True)
    activity = models.CharField(default=0,max_length=1,choices=ACTIVITY)
    education = models.CharField(max_length=1, null=True, blank=True, choices=EDUCATION)
    ageLevel = models.CharField(max_length=1, null=True, blank=True, choices=AGE_LEVEL)
    skillLevel= models.CharField(max_length=1, null=True, blank=True, choices=PROGRAMING)
    # USERNAME_FIELD = 'phone'  # Use phone as the username


    class Meta:
        verbose_name = "دانشجو"  # Singular name for admin
        verbose_name_plural = "دانشجو ها"  # Plural name for admin
    def __str__(self):
        return f"Student: {self.first_name} {self.last_name}"