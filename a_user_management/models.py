from django.contrib.auth.models import AbstractUser
from django.db import models
from a_institution_management.models import Branch, Institution
# Create your models here.



class Person(AbstractUser):
    code_melli = models.CharField(max_length=10, null=True)
    phone = models.CharField(max_length=11, null=True)
    date_of_birth = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)       # Automatically updated on every save
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

class Owner(Person):
    institution = models.OneToOneField(Institution, on_delete=models.CASCADE, related_name='owner', null=True)

    def __str__(self):
        return f"Owner: {self.first_name} {self.last_name} at {self.institution.full_name}"
    
    


class Admin(Person): 
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='admins', null=True)
    branch = models.OneToOneField(Branch, on_delete=models.CASCADE, related_name='admin', null=True)

    def __str__(self):
        return f"Admin: {self.first_name} {self.last_name} at {self.branch.name}"
    


class Employee(Person):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='employees', null=True)    
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='employees', null=True)

    def __str__(self):
        return f"Employee: {self.first_name} {self.last_name} at {self.branch.name}"
    

class Teacher(Person):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='teachers', null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='teachers', null=True)

    def __str__(self):
        return f"Teacher: {self.first_name} {self.last_name} at {self.branch.name}"
    

class Student(Person):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='students', null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='students', null=True)

    def __str__(self):
        return f"Student: {self.first_name} {self.last_name} at {self.branch.name}"