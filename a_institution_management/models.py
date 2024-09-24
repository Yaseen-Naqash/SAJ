from django.db import models


# Create your models here.
class Institution(models.Model):
    full_name = models.CharField(max_length=255, null=True)
    abbreviation_name = models.CharField(max_length=15, null=True)
    


class Branch(models.Model):
    name = models.CharField(max_length=255, null=True)
    Institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='branches', null=True)
    address = models.CharField(max_length=511, null=True)
    latitude = models.CharField(max_length=63, null=True)
    longitude = models.CharField(max_length=63, null=True)