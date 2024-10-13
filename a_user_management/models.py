from django.contrib.auth.models import AbstractUser
from django.db import models
from a_institution_management.models import Branch
import random
from django.utils import timezone

class Person(AbstractUser):
    code_melli = models.CharField(max_length=10, null=True, blank=True, verbose_name="کد ملی")
    phone = models.CharField(max_length=11, null=True, unique=True, blank=True, verbose_name="تلفن همراه")
    phone2 = models.CharField(max_length=11, null=True, unique=True, blank=True, verbose_name="تلفن همراه 2")

    date_of_birth = models.DateField(null=True, blank=True, verbose_name="تاریخ تولد")
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)       # Automatically updated on every save
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True, verbose_name="تصویر پروفایل")
    

class PhoneVerification(models.Model):
    phone_number = models.CharField(max_length=11,null=True, blank=True)  # Adjust length as necessary
    verification_code = models.CharField(max_length=4, null=True, blank=True)  # Assuming 4-digit code
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):

        return timezone.now() > self.created_at + timezone.timedelta(seconds=120)
    
    class Meta:
        verbose_name = "تاییدیه شماره"  # Singular name for admin
        verbose_name_plural = " تاییدیه شماره ها"  # Plural name for admin

    def generate_code(self):
        self.verification_code = str(random.randint(1000, 9999))


class Employee(Person):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='employees', null=True, blank=True)

    class Meta:
        verbose_name = "کارمند" 
        verbose_name_plural = "کارمندان"  
    def __str__(self):
        return f"کارمند {self.first_name} {self.last_name}"
    

class Teacher(Person):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='teachers', null=True, blank=True)



    class Meta:
        verbose_name = "استاد"  
        verbose_name_plural = "اساتید"  
    def __str__(self):
        return f"استاد {self.first_name} {self.last_name}"
    



class Grade(models.Model):
    title = models.CharField(max_length=127, null=True, blank=True)
    gradeLevel = models.IntegerField(default=0)
    

    class Meta:
        verbose_name = "سطح"  # Singular name for admin
        verbose_name_plural = "سطوح"  # Plural name for admin
    def __str__(self):
        return f'{self.title}'

class Student(Person):
    ACTIVITY = [
        ('0','در حال تحصیل'),
        ('1','پایان دوره'),
        ('2','معلق'),

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

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='students', null=True, blank=True, verbose_name="شعبه")
    grade = models.ForeignKey(Grade,on_delete=models.CASCADE, related_name='students', null=True, blank=True, verbose_name="سطح")
    activity = models.CharField(default=0,max_length=1,choices=ACTIVITY, verbose_name="وضعیت")
    education = models.CharField(max_length=1, null=True, blank=True, choices=EDUCATION, verbose_name="تحصیلات")
    ageLevel = models.CharField(max_length=1, null=True, blank=True, choices=AGE_LEVEL, verbose_name="رده سنی")
    # USERNAME_FIELD = 'phone'  # Use phone as the username


    class Meta:
        verbose_name = "دانشجو"  # Singular name for admin
        verbose_name_plural = "دانشجو ها"  # Plural name for admin
    def __str__(self):
        return f"{self.first_name} {self.last_name}"