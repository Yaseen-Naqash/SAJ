from django.db import models
from a_user_management.models import Person
from a_course_management.models import Section
from a_institution_management.models import Branch
# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=63, null=True, blank=True)
    description = models.TextField(max_length=4095, null=True, blank=True)
    news_img = models.ImageField(upload_to='News_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)   
    author = models.ForeignKey(Person, on_delete=models.SET_NULL, related_name='news', null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, related_name='news')

    class Meta:
        verbose_name = "خبر" 
        verbose_name_plural = "اخبار" 

    def __str__(self):
        return f"خبر: {self.title} از {self.author.first_name} {self.author.last_name}"
    
class Notification(models.Model):
    title = models.CharField(max_length=63, null=True, blank=True)
    description = models.TextField(max_length=4095, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)   
    author = models.ForeignKey(Person, on_delete=models.SET_NULL, related_name='notification', null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, related_name='notification', null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, related_name='notifications')

    def __str__(self):
        return f"اطلاعیه: {self.title} از {self.author.first_name} {self.author.last_name}"
    
    class Meta:
        verbose_name = "اطلاعیه" 
        verbose_name_plural = "اطلاعیه ها" 
    
 