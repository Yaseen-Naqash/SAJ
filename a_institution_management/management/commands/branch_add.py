from django.core.management.base import BaseCommand
from a_financial_management.models import Receipt
from a_institution_management.models import Branch
import random
class Command(BaseCommand):
    help = 'Create dummy data for the database'

    def handle(self, *args, **kwargs):
        receipts = Receipt.objects.all()
        branches = list(Branch.objects.all())

        for receipt in receipts:


            receipt.branch = branches[random.randint(0, 1)]
            receipt.save()
            
        self.stdout.write("done")