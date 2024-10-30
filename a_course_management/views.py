from django.shortcuts import get_object_or_404, render
from .models import Course, Degree
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
        for section in sections:
            section.attendance_count = section.attendances.filter(
                section_student__student=student, status=False
            ).count()

    context = {'sections':sections, 'student':student}
    return render(request,'my_courses.html',context)

def my_degrees(request):
    student = request.user.student
    degrees = Degree.objects.filter(student = student)
    
    return render(request, 'my_degrees.html')