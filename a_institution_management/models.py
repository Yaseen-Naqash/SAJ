from django.db import models


# Create your models here.


class Branch(models.Model):
    name = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=511, null=True)
    latitude = models.CharField(max_length=63, null=True)
    longitude = models.CharField(max_length=63, null=True)

    class Meta:
        verbose_name = "شعبه" 
        verbose_name_plural = "شعب" 
    def __str__(self):
        return self.name