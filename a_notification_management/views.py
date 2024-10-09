from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from a_user_management.models import Student
from a_notification_management.models import Notification, News
from django.contrib import messages

# Create your views here.



@login_required
def home(request):

    student = None
    if hasattr(request.user, 'student'):
        student = request.user.student
    else:
        messages.error(request,'لطفا با یک حساب به عنوان دانشجو وارد شوید!')
        return redirect('student_login_url')
    
    news = News.objects.all()


    notifs = Notification.objects.filter(section__in=student.sections.all())


    context = {'news':news, 'notifs':notifs}
    return render(request,'home.html',context)
    