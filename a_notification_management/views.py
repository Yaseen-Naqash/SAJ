from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from a_user_management.models import Student
from a_notification_management.models import Notification, News

# Create your views here.



@login_required
def home(request):

    student = None
    if hasattr(request.user, 'student'):
        student = request.user.student
    
    news = News.objects.all()


    notifs = Notification.objects.filter(section__in=student.sections.all())


    context = {'news':news, 'notifs':notifs}
    return render(request,'home.html',context)
    