from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import EmailMessage
from django_countries.fields import CountryField

# @receiver(post_save,sender=settings.AUTH_USER_MODEL)
# def send_user_data_when_created_by_admin(sender, instance, **kwargs):
#     import pdb;pdb.set_trace()
#     if instance.user.role == 'shop':
#         first_name = instance.user.first_name
#         print('first name is',first_name)
#         last_name = instance.user.last_name
#         address = instance.address
#         email = instance.user.email
#         html_content = "your first name:%s <br> last name:%s <br> address:%s"
#         message=EmailMessage(subject='welcome',body=html_content %(first_name,last_name,address),to=[email])
#         message.content_subtype='html'
#         message.send()


# Create your models here.
class User(AbstractUser):
    USER_ROLE = (
        ('admin', 'Admin'),
        ('shop', 'Shop User'),
        ('customer', 'Customer'),
    )
    role =  models.CharField(max_length=20, choices=USER_ROLE, default='customer')
    allow_by_admin = models.BooleanField(default=False)
    street = models.CharField(max_length=30, blank=True)
    street1 = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    country = CountryField(max_length=30, blank=True)

