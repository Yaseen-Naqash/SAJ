from django.db import models
import uuid
from a_user_management.models import Person

import jdatetime
import random
# Create your models here.

def generate_custom_id():
    # Get the current Jalali date and time
    now = jdatetime.datetime.now()
    # Format the ID string using the Jalali date and time
    custom_id = f"APh.R-y{now.year}-mo{now.month:02d}-d{now.day:02d}-h{now.hour:02d}-mi{now.minute:02d}-s{now.second:02d}-{random.randint(1000,9999)}"
    return custom_id

class Receipt(models.Model):

    receipt_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # 3e5f3f76-ea8d-49b9-a34f-84392b74bc0b

    # receipt_id = models.CharField(max_length=63, editable=False, default=generate_custom_id)
    # APh.R-y1403-mo07-d25-h14-mi45-s30-8374

    title = models.CharField(max_length=63, null=True, blank=True, verbose_name='عنوان')
    description = models.TextField(max_length=511, null=True, blank=True, verbose_name='توضیحات')
    transaction_id = models.CharField(max_length=63, unique=True, null=True, blank=True, verbose_name='شماره پیگیری')
    amount = models.DecimalField(max_digits=11, decimal_places=0, null=True, verbose_name='(تومان) مبلغ')
    payer = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='پرداخت کننده')
    sender_account = models.CharField(max_length=63, null=True, blank=True, verbose_name='ارسال شده از حساب')
    receiver_account = models.CharField(max_length=63, null=True, blank=True, verbose_name='دریافت شده در حساب')
    created_method = models.CharField(max_length=1, choices=[('0', 'اتوماتیک'), ('1', 'دستی')], default='1', verbose_name='روش ثبت')
    payment_method = models.CharField(max_length=1, choices=[('0', 'کارتخوان'), ('1', 'کارت به کارت'), ('2', 'نقدی'), ('3', 'درگاه پرداخت')], default='0', verbose_name='روش پرداخت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')
    updated_at = models.DateTimeField(auto_now=True)
    jdate = models.CharField(max_length=15, default=jdatetime.date.today().strftime('%Y/%m/%d'), verbose_name='تاریخ')


    class Meta:
        verbose_name = "رسید مالی"  # Singular name for admin
        verbose_name_plural = "رسید های مالی"  # Plural name for admin
    def __str__(self):
        return f"مبلغ {self.amount} تومان از {self.payer}"

# 999,999,999.00