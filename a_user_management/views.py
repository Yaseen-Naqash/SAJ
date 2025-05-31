import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from a_user_management.models import Student, PhoneVerification, Teacher, Grade
from a_course_management.models import Degree
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

from django.utils import timezone
import jdatetime

    
# Create your views here.



def calculate_age(birth_day_date):
    # Convert the Jalali birthday date string to a Jalali date
    birth_day_date_jalali = jdatetime.datetime.strptime(birth_day_date, "%d. %m. %Y").date()
    
    # Convert Jalali date to Gregorian date
    birth_day_date_gregorian = birth_day_date_jalali.togregorian()  # Correct method to convert to Gregorian

    current_date_gregorian = timezone.now().date()

    # Calculate age
    age = current_date_gregorian.year - birth_day_date_gregorian.year

    if (current_date_gregorian.month, current_date_gregorian.day) < (birth_day_date_gregorian.month, birth_day_date_gregorian.day):
        age -= 1

    return age

def logout_command(request):

    
    logout(request)
    return redirect('login_url')

def login_view(request):
    if request.method == 'POST':


        phone = request.POST.get('username')
        password = request.POST.get('password')


        try:
            student = Student.objects.get(username=phone)
        except Student.DoesNotExist:
            messages.error(request, 'خطا : اطلاعات شما اشتباه است.')  
            return redirect('   login_url')  

        if student and student.password == password:
            login(request, student)
            messages.success(request, 'موفق : شما با موفقیت وارد شدید.')
            return redirect('home_url')  
        else:
            messages.error(request, 'خطا : اطلاعات شما اشتباه است.')  

    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        password = request.POST.get('codeMelli')
        codeMelli = request.POST.get('codeMelli')
        birthDayDate = request.POST.get('birthDayDate')
        phone = request.POST.get('phone')
        phone2 = request.POST.get('phone2')
        confirmationCode = request.POST.get('confirmationCode')
        education = request.POST.get('educations')
        primaryState = request.POST.get('primaryState')
        birthDayDate_formatted = datetime.strptime(birthDayDate, "%d. %m. %Y").date()

        age = calculate_age(birthDayDate)

        if age <= 9:
            ageLevel = '0'
        elif 9 < age <= 14:
            ageLevel = '1'
        else:
            ageLevel = '2'

        if primaryState is None:
            skillLevel = 1
        else:
            skillLevel = 0
        

        if verify_code(phone, confirmationCode):
            student = Student.objects.create(
                first_name=firstName,
                last_name=lastName,
                password=password,
                phone=phone,
                phone2=phone2,
                username=phone,
                code_melli=codeMelli,
                date_of_birth=birthDayDate_formatted,
                education=education,
                ageLevel = ageLevel,
            )
            messages.success(request, 'موفق : اکانت شما ساخته شد.')

            return redirect('login_url')
        else:
            messages.error(request, 'کد تایید ارسال شده به تلفن شما معتبر نیست')

        
        
    context = {}
    return render(request,'register.html',context)

def generate_verification_code(phone_number):
    verification = PhoneVerification(phone_number=phone_number)
    verification.generate_code()
    verification.save()
    return verification.verification_code

def verify_code(phone_number, code):

    verification = PhoneVerification.objects.filter(phone_number=phone_number).order_by('-created_at').first()
    if verification is None:
        return False
    if verification.is_expired():
        return False
    
    if verification.verification_code == code:
        return True
    else:
        return False

def send_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        phone_number = data.get('phone_number')

        # Your logic for sending the verification code goes here
        code = generate_verification_code(phone_number)
        # For example, you could use Twilio or another SMS service to send the code
        print(code)
        if phone_number:
            # Assuming the logic is successful
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid phone number'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})

def my_degrees(request):
    student = request.user.student
    degrees = Degree.objects.filter(student = student)
    context = {'degrees':degrees, }
    return render(request,'my_degrees.html',context)