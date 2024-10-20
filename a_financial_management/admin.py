from django.contrib import admin
from .models import Receipt
from django.db.models import Sum  # This is the missing import

from django.utils import timezone
from datetime import timedelta
from django.contrib.admin import SimpleListFilter

import jdatetime
import django_jalali.admin as jadmin # jalali date picker
from django.template.loader import render_to_string
# from jalali_date import datetime2jalali, date2jalali, jalali_to_gregorian  # To handle Jalali-Gregorian conversions
from datetime import datetime
from django import forms
# from jalali_date.admin import widgets as jadmin
# from jalali_date import date2jalali, datetime2jalali
# from jalali_date import datetime, date  # These are helper classes for Jalali date handling

# Register your models here.

class JalaliDateRangeForm(forms.Form):
    start_date = forms.DateField(
        widget=jadmin.widgets.AdminjDateWidget, 
        required=False,
        label='از تاریخ',
    )
    end_date = forms.DateField(
        widget=jadmin.widgets.AdminjDateWidget, 
        required=False,
        label='تا تاریخ',
    )
    debug_input = forms.CharField(
        required=False,
        label='Debug Input',
        widget=forms.TextInput(attrs={'placeholder': 'Test Input'})  # Optional placeholder
    )


class JalaliDateRangeFilter(SimpleListFilter):
    title = 'بازه زمانی'  # Title for your filter in the admin panel
    parameter_name = 'created_at_range'

    template = 'admin/jalali_date_range_filter.html'  # You'll need to create this template

    def lookups(self, request, model_admin):
        return (
            ('today', 'امروز'),
            ('yesterday', 'دیروز'),
            ('last_7_days', '7 روز گزشته'),
            ('last_month', '30 روز گزشته'),
            ('last_year', 'یک سال گزشته'),
        )  # Empty, since we will be using form fields for input


    
    def queryset(self, request, queryset):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')


    
        def jalali_to_gregorian(jalali_year, jalali_month, jalali_day):
            # This is a simple function, you may need to adjust for proper conversion
            # Here’s a placeholder for the conversion logic
            # You may want to replace it with an accurate algorithm or library
            import jdatetime  # Using the jdatetime library for conversion

            jalali_date = jdatetime.date(jalali_year, jalali_month, jalali_day)
            return jalali_date.togregorian()
        
        if start_date:
            start_date_formatted = datetime.strptime(start_date, "%d. %m. %Y").date()
            jalali_year = start_date_formatted.year
            jalali_month = start_date_formatted.month
            jalali_day = start_date_formatted.day

            start_gregorian_date = jalali_to_gregorian(jalali_year, jalali_month, jalali_day)
            print(start_gregorian_date)  # Check the converted Gregorian date
            queryset = queryset.filter(created_at__gte=start_gregorian_date)

        if end_date:
            end_date_formatted = datetime.strptime(end_date, "%d. %m. %Y").date()
            jalali_year = end_date_formatted.year
            jalali_month = end_date_formatted.month
            jalali_day = end_date_formatted.day

            end_gregorian_date = jalali_to_gregorian(jalali_year, jalali_month, jalali_day)
            print(end_gregorian_date)  # Check the converted Gregorian date
            queryset = queryset.filter(created_at__lte=end_gregorian_date)

        return queryset


    def choices(self, changelist):
        context = {
            'form': JalaliDateRangeForm(),
        }
        return render_to_string(self.template, context) 



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
        JalaliDateRangeFilter,
        
    )


    search_fields = ['title', 'payer', 'sender_account', 'jdate']  # Define searchable fields for Student
    change_list_template = 'admin/receipt_changelist.html'  # Custom template to show the totals


    def changelist_view(self, request, extra_context=None):
        # Call the super method first to generate the response
        response = super().changelist_view(request, extra_context=extra_context)
        
        
        try:
            qs = response.context_data['cl'].queryset  # Get the queryset displayed in the changelist
        except (AttributeError, KeyError) as e:
            print(f"Error accessing context data: {e}")
            return response
        
        # Calculate the total sum of the 'amount' field in the queryset
        total = qs.aggregate(total=Sum('amount'))['total'] or 0
        

        # Add the total to the extra_context and update the response context
        if extra_context is None:
            extra_context = {}
        extra_context['total'] = total
        response.context_data.update(extra_context)
        
        return response