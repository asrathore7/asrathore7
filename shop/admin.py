from django.contrib import admin
from .models.shops import *
from .models.products import *
# Register your models here.

admin.site.register(Shop)
admin.site.register(Product)
