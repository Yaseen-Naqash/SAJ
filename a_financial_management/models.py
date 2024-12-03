from django.db import models
import uuid
from a_user_management.models import Student
from django.utils import timezone
from datetime import timedelta
import jdatetime
import random
# Create your models here.

def generate_custom_id():
    # Get the current Jalali date and time
    now = jdatetime.datetime.now()
    # Format the ID string using the Jalali date and time
    custom_id = f"APh.R-y{now.year}-mo{now.month:02d}-d{now.day:02d}-h{now.hour:02d}-mi{now.minute:02d}-s{now.second:02d}-{random.randint(1000,9999)}"
    return custom_id





class ReceiptQuerySet(models.QuerySet):
    def today(self):
        today = timezone.now().date()
        return self.filter(created_at__date=today)

    def yesterday(self):
        yesterday = timezone.now().date() - timedelta(days=1)
        return self.filter(created_at__date=yesterday)

    def last_7_days(self):
        return self.filter(created_at__date__gte=timezone.now() - timedelta(days=7))

    def last_month(self):
        # Get today's date
        today = timezone.now().date()
        
        # Get the first day of the current month
        first_day_of_current_month = today.replace(day=1)
        
        # Subtract one day to get the last day of the previous month
        last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
        
        # Now get the first day of that last month
        first_day_of_last_month = last_day_of_last_month.replace(day=1)
        
        # Filter receipts for the previous month
        return self.filter(created_at__date__gte=first_day_of_last_month, created_at__date__lte=last_day_of_last_month)

    def last_2_months(self):
        today = timezone.now().date()
        first_day_of_current_month = today.replace(day=1)
        last_month_end = first_day_of_current_month - timedelta(days=1)
        two_months_ago_start = last_month_end.replace(day=1) - timedelta(days=last_month_end.day)
        return self.filter(created_at__date__gte=two_months_ago_start)

    def last_6_months(self):
        six_months_ago = timezone.now() - timedelta(days=6 * 30)
        return self.filter(created_at__date__gte=six_months_ago)

    def last_year(self):
        today = timezone.now().date()
        return self.filter(created_at__date__gte=today.replace(year=today.year - 1))

class Receipt(models.Model):

    PAYMENT_METHOD = [
        ('0', 'کارتخوان'),
        ('1', 'کارت به کارت'),
        ('2', 'نقدی'), 
        ('3', 'درگاه پرداخت'), 
        ('4', 'تخفیفی'),
    ]


    receipt_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # 3e5f3f76-ea8d-49b9-a34f-84392b74bc0b

    # receipt_id = models.CharField(max_length=63, editable=False, default=generate_custom_id)
    # APh.R-y1403-mo07-d25-h14-mi45-s30-8374

    title = models.CharField(max_length=63, null=True, verbose_name='عنوان')
    transaction_id = models.CharField(max_length=63, unique=True, null=True, blank=True, verbose_name='شماره پیگیری')
    formatted_amount = models.CharField(max_length=127, null=True, verbose_name='(تومان) مبلغ')

    amount = models.DecimalField(max_digits=11, decimal_places=0, null=True, verbose_name='(تومان) مبلغ')
    payer = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, verbose_name='پرداخت کننده')
    # sender_account = models.CharField(max_length=63, null=True, blank=True, verbose_name='ارسال شده از حساب')
    # receiver_account = models.CharField(max_length=63, null=True, blank=True, verbose_name='دریافت شده در حساب')
    created_method = models.CharField(max_length=1, choices=[('0', 'اتوماتیک'), ('1', 'دستی')], default='1', verbose_name='روش ثبت')
    payment_method = models.CharField(max_length=1, choices=PAYMENT_METHOD, default='0', verbose_name='روش پرداخت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')
    updated_at = models.DateTimeField(auto_now=True)
    jdate = models.CharField(max_length=15, default=jdatetime.date.today().strftime('%Y/%m/%d'), verbose_name='تاریخ')
    confirmed = models.BooleanField(default=False, verbose_name='تایید شده')
    description = models.TextField(max_length=511, default='', null=True, blank=True, verbose_name='توضیحات')


    def save(self, *args, **kwargs):
        if self.formatted_amount:
            # Remove commas and convert the formatted amount to an integer
            numeric_value = int(self.formatted_amount.replace(",", ""))
            self.amount = numeric_value
        else:
            self.amount = None  # Handle empty or invalid input as needed



        super().save(*args, **kwargs)

        if self.payment_method == '4' and self.payer:
            self.payer.balance += self.amount
            self.payer.save()  # Save the updated payer's balance


    objects = ReceiptQuerySet.as_manager()
    class Meta:
        verbose_name = "رسید مالی"  # Singular name for admin
        verbose_name_plural = "رسید های مالی"  # Plural name for admin
        ordering = ['confirmed', '-created_at']
    def __str__(self):
        return f"مبلغ {self.amount} تومان از {self.payer}"

# 999,999,999.00