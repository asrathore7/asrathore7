'''Shop admin register'''
from django.contrib import admin
from .models.shops import Shop
from .models.products import Product


admin.site.register(Shop)
admin.site.register(Product)
