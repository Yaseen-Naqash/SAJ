
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Student  # Assuming your model is named Student

@shared_task
def update_inactive_students():
    # Get the date 60 days ago
    sixty_days_ago = timezone.now() - timedelta(days=60)

    # Find users who haven't logged in for 60 days
    inactive_students = Student.objects.filter(last_login__lt=sixty_days_ago, activity='0')

    # Update their activity status to '1'
    inactive_students.update(activity='1')
