from django.shortcuts import render

# Create your views here.


def students_login(request):
    context = {}
    return render(request,'login.html',context)