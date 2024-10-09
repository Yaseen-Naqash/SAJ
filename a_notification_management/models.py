from django.db import models
from a_user_management.models import Person
from a_course_management.models import Section
# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=63, null=True, blank=True)
    description = models.TextField(max_length=4095, null=True, blank=True)
    news_img = models.ImageField(upload_to='News_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)   
    author = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='news', null=True, blank=True)

    def __str__(self):
        return f"News: {self.title} from {self.author.first_name} {self.author.last_name}"
    
class Notification(models.Model):
    title = models.CharField(max_length=63, null=True, blank=True)
    description = models.TextField(max_length=4095, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)   
    author = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='notification', null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='notification', null=True, blank=True)

    def __str__(self):
        return f"Notification: {self.title} from {self.author.first_name} {self.author.last_name}"
    
 