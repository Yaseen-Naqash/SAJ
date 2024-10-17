from django.contrib import admin
from .models import Receipt
# Register your models here.
#STUDENT
@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):

    list_display = (
        'title', 
        'transaction_id', 
        'amount',
        'payment_method',
        'sender_account',
        'payer', 
        'jdate',
    )
    
    list_filter = (
        'payment_method',
        'created_at',
        
    )

    search_fields = ['title', 'payer', 'sender_account', 'jdate']  # Define searchable fields for Student


