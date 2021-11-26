from django.db import models
from django.contrib.auth.models import AbstractUser
    
# Create your models here.
class User(AbstractUser):
    USER_ROLE = (
        ('admin', 'Admin'),
        ('shop', 'Shop User'),
        ('customer', 'Customer'),
    )
    role =  models.CharField(max_length=20, choices=USER_ROLE, default='customer')
    allow_by_admin = models.BooleanField(default=False)
