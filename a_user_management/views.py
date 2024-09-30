import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from a_user_management.models import Student
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def home(request):

    # # Success message
    # messages.success(request, 'موفق : اکانت شما ساخته شد.')

    # # Error message
    # messages.error(request, 'خطا : شماره اشتباه است.')

    # # Info message
    # messages.info(request, 'This is some information.')

    # # Warning message
    # messages.warning(request, 'This is a warning.')


    context = {}
    return render(request,'base.html',context)

def logout_command(request):
    logout(request)
    return redirect('student_login_url')


def students_login(request):
    if request.method == 'POST':
        phone = request.POST.get('username')
        password = request.POST.get('password')
        student = Student.objects.get(phone=phone)
        if student and student.password == password:
            login(request, student)
            messages.success(request, 'موفق : شما با موفقیت وارد شدید.')
            return redirect('home')  
        else:
            messages.error(request, 'خطا : اطلاعات شما اشتباه است.')  

    context = {'login_method': 'student'}
    return render(request, 'login.html', context)



def teachers_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    context = {'login_method':'teacher'}
    return render(request,'login.html',context)

def register(request):
    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        confirmationCode = request.POST.get('confirmationCode')
        phone = request.POST.get('phone')
        if password != confirmPassword:
            print(password)
            print(confirmPassword)
            messages.error(request, 'خطا : تکرار رمز عبور اشتباه است.')
            return redirect('register_url') 

        

        # Create the student instance
        student = Student.objects.create(
            first_name=firstName,
            last_name=lastName,
            password=confirmPassword,  # Store hashed password
            phone=phone,
            username=phone,
        )
        messages.success(request, 'موفق : اکانت شما ساخته شد.')

        # Redirect to a success page or login page
        return redirect('student_login_url')
        
        
    context = {}
    return render(request,'register.html',context)

def send_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        phone_number = data.get('phone_number')

        # Your logic for sending the verification code goes here
        # For example, you could use Twilio or another SMS service to send the code

        if phone_number:
            # Assuming the logic is successful
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid phone number'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})