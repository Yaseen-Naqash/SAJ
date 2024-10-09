from django.shortcuts import get_object_or_404, render
from .models import Course
# Create your views here.
def courses(request):
    courses = Course.objects.all()
    context = {'courses':courses}
    return render(request,'course.html',context)

def course_detail(request,pk):
    course = get_object_or_404(Course, pk=pk)  # Fetch course by pk
    context = {'course':course}
    return render(request,'course_detail.html',context)

def my_courses(request):

    student = None
    if hasattr(request.user, 'student'):
        student = request.user.student  

    sections = student.sections.all()
    print(sections)

    context = {'sections':sections}
    return render(request,'my_courses.html',context)