from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
def set_dropdown_value(request):
    if request.method == "POST":
        data = json.loads(request.body)
        value = data.get("value", "")
        # Clear old value and set new one
        request.session["branch"] = value
        # print(request.session["branch"])
        return JsonResponse({"status": "success"})
    
        
    return JsonResponse({"status": "failed"}, status=400)
