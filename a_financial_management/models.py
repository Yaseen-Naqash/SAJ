from django.db import models
import uuid
from a_user_management.models import Student
from a_course_management.models import Section
from django.utils import timezone
from datetime import timedelta
import jdatetime
import random
from a_institution_management.models import Branch
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
    REASON = [
        
        ('0', "بابت قسط شهریه"),
        ('1', "بابت شهریه"),
        ('2', "بابت کلاس تقویتی"), 
        ('3', "بابت کمک به آموزشگاه"), 
        ('4', "بابت خسارت"),
        ('5', "نامشخص"),
        ('6', "شارژ کیف پول"),


    ]


    receipt_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # 3e5f3f76-ea8d-49b9-a34f-84392b74bc0b

    time_stamp = models.CharField(max_length=63, editable=False, default=generate_custom_id)
    # APh.R-y1403-mo07-d25-h14-mi45-s30-8374

    title = models.CharField(max_length=63, null=True, verbose_name='عنوان')
    transaction_id = models.CharField(max_length=63, unique=True, null=True, blank=True, verbose_name='شماره پیگیری')
    formatted_amount = models.CharField(max_length=127, null=True, verbose_name='(تومان) مبلغ')
    reason = models.CharField(max_length=1, choices=REASON, null=True, blank=True, default='5', verbose_name='بابت')
    section = models.ForeignKey(Section, related_name='receipts', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='دوره')
    amount = models.IntegerField(null=True, verbose_name='(تومان) مبلغ')
    payer = models.ForeignKey(Student, related_name='receipts', on_delete=models.SET_NULL, null=True, verbose_name='پرداخت کننده')
    # sender_account = models.CharField(max_length=63, null=True, blank=True, verbose_name='ارسال شده از حساب')
    # receiver_account = models.CharField(max_length=63, null=True, blank=True, verbose_name='دریافت شده در حساب')
    created_method = models.CharField(max_length=1, choices=[('0', 'اتوماتیک'), ('1', 'دستی')], default='1', verbose_name='روش ثبت')
    payment_method = models.CharField(max_length=1, choices=PAYMENT_METHOD, default='0', verbose_name='روش پرداخت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')
    updated_at = models.DateTimeField(auto_now=True)
    jdate = models.CharField(max_length=15, default=jdatetime.date.today().strftime('%Y/%m/%d'), verbose_name='تاریخ')
    confirmed = models.BooleanField(default=False, verbose_name='تایید شده')
    description = models.TextField(max_length=511, default='', null=True, blank=True, verbose_name='توضیحات')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, related_name='receipts')


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


from a_course_management.models import SectionStudent
from django.db.models.signals import pre_save
from django.dispatch import receiver
@receiver(pre_save, sender=Receipt)
def calculate_balance_and_dept(sender, instance, **kwargs):
    if not instance.pk:  # Only for new instances (pk doesn't exist yet)
        if instance.section and instance.payer:
            try:
                # Get the SectionStudent record
                section_student = SectionStudent.objects.get(
                    section=instance.section,
                    student=instance.payer,
                    activity='0'
                )
                
                receipt_amount = instance.amount
                current_dept = section_student.dept
                
                if current_dept > 0:
                    if receipt_amount >= current_dept:
                        # Pay off entire debt and add excess to balance
                        excess = receipt_amount - current_dept
                        section_student.dept = 0
                        instance.payer.balance += excess
                        print('1. amount added : ')
                        print(instance.payer.balance)
                    else:
                        # Partially pay debt (no balance change)
                        section_student.dept -= receipt_amount
                    
                    # Save changes
                    section_student.save(update_fields=['dept'])
                    instance.payer.save(update_fields=['balance'])
                    
            except SectionStudent.DoesNotExist:
                # Handle case where SectionStudent doesn't exist
                pass
            except Exception as e:
                # Handle other potential errors
                print(f"Error processing receipt: {e}")

    else: # Receipt update
        try:
            old_receipt = Receipt.objects.get(pk=instance.pk)
            if old_receipt.amount != instance.amount:
                section_student = SectionStudent.objects.get(
                    section=instance.section,
                    student=instance.payer,
                    activity='0'
                )
                
                old_amount = old_receipt.amount
                new_amount = instance.amount
                difference = new_amount - old_amount
                max_dept = section_student.section.course.price
                current_dept = section_student.dept
                
                # CASE 1: Payment increased
                if difference > 0:
                    if current_dept > 0:
                        # Apply to debt first
                        remaining_dept = min(difference, current_dept)
                        section_student.dept -= remaining_dept
                        excess = difference - remaining_dept
                        if excess > 0:
                            instance.payer.balance += excess
                
                # CASE 2: Payment decreased
                elif difference < 0:
                    amount_to_restore = abs(difference)
                    available_debt_capacity = max_dept - current_dept
                    
                    if available_debt_capacity >= amount_to_restore:
                        # Can fully restore to debt
                        section_student.dept += amount_to_restore
                    else:
                        # Partially restore debt and reduce balance
                        section_student.dept = max_dept
                        balance_reduction = amount_to_restore - available_debt_capacity
                        instance.payer.balance -= balance_reduction
                
                # Save changes
                section_student.save(update_fields=['dept'])
                instance.payer.save(update_fields=['balance'])
                
        except (Receipt.DoesNotExist, SectionStudent.DoesNotExist):
            pass  # Handle errors appropriately








    # Signal handler for Receipt model that automatically manages:
    # - Debt calculation (SectionStudent.dept)
    # - Balance adjustment (payer.balance)
    
    # Handles two scenarios:
    # 1. NEW RECEIPTS (creation):
    #    - Applies payment to outstanding debt first
    #    - Any excess amount is added to payer's balance
    #    - Partial payments only reduce debt (no balance change)
    
    # 2. UPDATED RECEIPTS (amount changes):
    #    - Recalculates debt and balance based on amount difference
    #    - If increasing payment:
    #      * Pays remaining debt first
    #      * Adds excess to balance
    #    - If decreasing payment:
    #      * Increases debt by the reduced amount
    #      * Doesn't affect balance (payment reversal)

    #     Special Cases:
    # - When reducing payment on a cleared debt:
    #   * Restores debt first (up to original price)
    #   * Only reduces balance if debt restoration is impossible
    # - Debt can never exceed original course price
    # - Balance can go negative if necessary
    
    # Error Handling:
    # - Silently skips if SectionStudent record doesn't exist
    # - Prints errors for debugging (but doesn't stop save operation)



