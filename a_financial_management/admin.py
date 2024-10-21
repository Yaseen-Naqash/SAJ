from django.contrib import admin
from .models import Receipt
from django.db.models import Sum  
from django.utils import timezone
from datetime import timedelta
from django.contrib.admin import SimpleListFilter
import jdatetime
from django.template.response import TemplateResponse
from datetime import datetime

class JalaliDateRangeFilter(SimpleListFilter):
    title = 'بازه زمانی'  # Title for your filter in the admin panel
    parameter_name = 'created_at_range'
    template = 'admin/jalali_date_range_filter.html'  # You'll need to create this template


    def lookups(self, request, model_admin):
        return (
            ('test', 'test'),
            ('test', 'test'),

        )  # values are dummy data just to prevent some errors and show my form

    def queryset(self, request, queryset):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date is not None:
            request.session['start_date'] = start_date


        if end_date is not None:
            request.session['end_date'] = end_date
            
        return queryset






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

        def jalali_to_gregorian(jalali_year, jalali_month, jalali_day):
            # This is a simple function, you may need to adjust for proper conversion
            # Here’s a placeholder for the conversion logic
            # You may want to replace it with an accurate algorithm or library

            jalali_date = jdatetime.date(jalali_year, jalali_month, jalali_day)
            return jalali_date.togregorian()
        
        # Retrieve the start_date and end_date from the session
        start_date = request.session.get('start_date')
        end_date = request.session.get('end_date')

        if start_date is not None and start_date != '':
            start_date_formatted = datetime.strptime(start_date, "%d. %m. %Y").date()
            jalali_year = start_date_formatted.year
            jalali_month = start_date_formatted.month
            jalali_day = start_date_formatted.day
            start_gregorian_date = jalali_to_gregorian(jalali_year, jalali_month, jalali_day)

            queryset = queryset.filter(created_at__gte=start_gregorian_date)
        if end_date is not None and end_date != '':
            end_date_formatted = datetime.strptime(end_date, "%d. %m. %Y").date()
            jalali_year = end_date_formatted.year
            jalali_month = end_date_formatted.month
            jalali_day = end_date_formatted.day
            end_gregorian_date = jalali_to_gregorian(jalali_year, jalali_month, jalali_day)

            queryset = queryset.filter(created_at__lte=end_gregorian_date)



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
        response = super().changelist_view(request, extra_context=extra_context)
        
        # Only proceed if the response is a TemplateResponse
        if isinstance(response, TemplateResponse):
            try:
                # Access the queryset from context data
                qs = response.context_data['cl'].queryset
            except (AttributeError, KeyError) as e:
                print(f"Error accessing context data: {e}")
                return response

            # Calculate the total amount
            total = qs.aggregate(total=Sum('amount'))['total'] or 0

            # Add the total to extra_context and update the response context
            if extra_context is None:
                extra_context = {}
            extra_context['total'] = total
            response.context_data.update(extra_context)

            

        return response