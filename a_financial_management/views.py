from django.shortcuts import render
from a_financial_management.models import Receipt
# Create your views here.
def financial(request):
    student = request.user.student

    records = Receipt.objects.filter(payer=student)
    context = {'records': records}
    return render(request, 'financial.html', context)