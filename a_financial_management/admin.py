from django.contrib import admin
from .models import Receipt
from django.db.models import Sum  # This is the missing import

from django.utils import timezone
from datetime import timedelta
from django.contrib.admin import SimpleListFilter
# Register your models here.







class CustomDateFilter(SimpleListFilter):
    title = 'روز'  # The title shown in the admin UI
    parameter_name = 'created_at'

    def lookups(self, request, model_admin):
        return (
            ('today', 'امروز'),
            ('yesterday', 'دیروز'),
            ('last_7_days', '7 روز گزشته'),
            ('last_month', '30 روز گزشته'),
            ('last_year', 'یک سال گزشته'),
        )

    def queryset(self, request, queryset):
        today = timezone.now().date()
        if self.value() == 'today':
            return queryset.filter(created_at__date=today)
        elif self.value() == 'yesterday':
            yesterday = today - timedelta(days=1)
            return queryset.filter(created_at__date=yesterday)
        elif self.value() == 'last_7_days':
            last_7_days = today - timedelta(days=7)
            return queryset.filter(created_at__date__gte=last_7_days)
        elif self.value() == 'last_month':
            last_month = today - timedelta(days=30)
            return queryset.filter(created_at__date__gte=last_month)
        elif self.value() == 'last_year':
            last_year = today - timedelta(days=365)
            return queryset.filter(created_at__date__gte=last_year)
        return queryset



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
        CustomDateFilter,
        
    )

    search_fields = ['title', 'payer', 'sender_account', 'jdate']  # Define searchable fields for Student
    change_list_template = 'admin/receipt_changelist.html'  # Custom template to show the totals


    def changelist_view(self, request, extra_context=None):
        # Call the super method first to generate the response
        response = super().changelist_view(request, extra_context=extra_context)
        
        # Debugging: Check if context_data and queryset are available
        try:
            qs = response.context_data['cl'].queryset  # Get the queryset displayed in the changelist
        except (AttributeError, KeyError) as e:
            print(f"Error accessing context data: {e}")
            return response  # Return the response without modification if there is an error
        
        # Calculate the total sum of the 'amount' field in the queryset
        total = qs.aggregate(total=Sum('amount'))['total'] or 0
        
        # Debugging: Check if total is calculated correctly
        print(f"Total amount calculated: {total}")

        # Add the total to the extra_context and update the response context
        if extra_context is None:
            extra_context = {}
        extra_context['total'] = total
        response.context_data.update(extra_context)
        
        return response