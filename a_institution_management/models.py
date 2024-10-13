from django.db import models


# Create your models here.


class Branch(models.Model):
    name = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=511, null=True)
    latitude = models.CharField(max_length=63, null=True)
    longitude = models.CharField(max_length=63, null=True)