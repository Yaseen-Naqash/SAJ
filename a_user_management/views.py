import json
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

def home(request):
    context = {}
    return render(request,'base.html',context)


def students_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    context = {'login_method':'student'}
    return render(request,'login.html',context)



def teachers_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    context = {'login_method':'teacher'}
    return render(request,'login.html',context)

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
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