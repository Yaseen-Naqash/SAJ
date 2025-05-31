from django.contrib.auth.models import AbstractUser
from django.db import models
from a_institution_management.models import Branch
import random
from django.utils import timezone
from django.contrib.auth.models import Group



class Person(AbstractUser):
    code_melli = models.CharField(max_length=10, null=True, verbose_name="کد ملی")
    phone = models.CharField(max_length=11, null=True, unique=True, verbose_name="تلفن همراه")
    phone2 = models.CharField(max_length=11, null=True, unique=True, blank=True, verbose_name="تلفن همراه 2")

    date_of_birth = models.DateField(null=True, verbose_name="تاریخ تولد")
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)       # Automatically updated on every save
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True, verbose_name="تصویر پروفایل")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class PhoneVerification(models.Model):
    phone_number = models.CharField(max_length=11,null=True, blank=True)  # Adjust length as necessary
    verification_code = models.CharField(max_length=4, null=True, blank=True)  # Assuming 4-digit code
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):

        return timezone.now() > self.created_at + timezone.timedelta(seconds=120)
    
    class Meta:
        verbose_name = "تاییدیه شماره"  # Singular name for admin
        verbose_name_plural = "تاییدیه شماره ها"  # Plural name for admin

    def generate_code(self):
        self.verification_code = str(random.randint(1000, 9999))



class Owner(Person):
    class Meta:
        verbose_name = "مالک" 
        verbose_name_plural = "5- مالکان"  

    def save(self, *args, **kwargs):
         # Check if the password needs hashing
        if not self.password.startswith('pbkdf2_'):  # Adjust based on your hashing algorithm
            self.set_password(self.password)  # Hash the password
        super().save(*args, **kwargs)  # Save the instance first

    def __str__(self):
        return f"مالک {self.first_name} {self.last_name}"
    

class Manager(Person):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='manager', null=True, blank=True)

    def save(self, *args, **kwargs):
         # Check if the password needs hashing
        if not self.password.startswith('pbkdf2_'):  # Adjust based on your hashing algorithm
            self.set_password(self.password)  # Hash the password
        super().save(*args, **kwargs)  # Save the instance first


    class Meta:
        verbose_name = "مدیر" 
        verbose_name_plural = "4- مدیران"  
    def __str__(self):
        return f"مدیر {self.first_name} {self.last_name}"

class Employee(Person):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='employees', null=True, blank=True)

    def save(self, *args, **kwargs):
         # Check if the password needs hashing
        if not self.password.startswith('pbkdf2_'):  # Adjust based on your hashing algorithm
            self.set_password(self.password)  # Hash the password
        super().save(*args, **kwargs)  # Save the instance first


    class Meta:
        verbose_name = "کارمند" 
        verbose_name_plural = "3- کارمندان"  
    def __str__(self):
        return f"کارمند {self.first_name} {self.last_name}"
    
class Teacher(Person):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='teachers', null=True, blank=True)

    def save(self, *args, **kwargs):
         # Check if the password needs hashing
        if not self.password.startswith('pbkdf2_'):  # Adjust based on your hashing algorithm
            self.set_password(self.password)  # Hash the password
        super().save(*args, **kwargs)  # Save the instance first


    class Meta:
        verbose_name = "استاد"  
        verbose_name_plural = "2- اساتید"  
    def __str__(self):
        return f"استاد {self.first_name} {self.last_name}"
    

class Grade(models.Model):
    title = models.CharField(max_length=127, null=True)
    gradeLevel = models.IntegerField(default=0)
    

    class Meta:
        verbose_name = "سطح" 
        verbose_name_plural = "سطوح"
    def __str__(self):
        return f'{self.title}'

class Student(Person):



    
    ACTIVITY = [
        ('0','در حال تحصیل'),
        ('1','در انتظار ثبت نام'),
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

    GENDER = [
        ('0','پسر'),
        ('1','دختر'),

    ]
    balance = models.IntegerField(default=0, null=True, verbose_name='(تومان) مبلغ')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='students', null=True, blank=True, verbose_name="شعبه")
    grade = models.ForeignKey(Grade,on_delete=models.CASCADE, related_name='students', null=True, blank=True, verbose_name="سطح")
    activity = models.CharField(default=0,max_length=1,choices=ACTIVITY, verbose_name="وضعیت")
    education = models.CharField(max_length=1, null=True, choices=EDUCATION, verbose_name="تحصیلات")
    ageLevel = models.CharField(max_length=1, null=True, choices=AGE_LEVEL, verbose_name="رده سنی")
    gender = models.CharField(max_length=1, null=True, choices=GENDER, verbose_name="جنسیت")

    # USERNAME_FIELD = 'phone'  # Use phone as the username

    @property
    def latest_course_title(self):
        latest_section_student = self.section_students.filter(activity='1').order_by('-id').first()
        if latest_section_student:
            return latest_section_student.section.course.title
        return "بدون دوره"

    class Meta:
        verbose_name = "دانشجو"  # Singular name for admin
        verbose_name_plural = "1- دانشجوها"  # Plural name for admin
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    


    