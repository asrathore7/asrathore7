from django.db import models
from django.conf import settings
from django.db.models import fields
from django_countries.fields import CountryField

# Create your models here.
class Shop(models.Model):
    shop_name = models.CharField(max_length=40)
    shop_owner = models.ForeignKey(settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, limit_choices_to={'role': 'shop'})
    image = models.ImageField(upload_to='shop_images', blank=True)
    street = models.CharField(max_length=50, blank=True)
    street1 = models.CharField(max_length=50, blank=True)
    pin_code = models.CharField(max_length=6, default="452001")
    city = models.CharField(max_length=20, blank=True)
    country = CountryField(blank=True)
    is_approved = models.BooleanField(default=False)
