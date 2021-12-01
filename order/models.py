from django.db import models
from django.conf import settings
from django.views.generic.edit import DeleteView
from shop.models.products import Product
from django.views.generic import CreateView, UpdateView, DeleteView

class SaleOrderLine(models.Model):
    
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    qty = models.IntegerField(blank=True)
    unit_price = models.FloatField(blank=True)
    subtotal = models.FloatField(blank=True)


class SaleOrder(models.Model):

    status = (
        ('new', 'New'),
        ('ship', 'shipped'),
        ('delivered', 'delivered'),
        ('cancel', 'Cancel'),
    )

    customer_id = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, limit_choices_to={'role': 'customer'})
    order_status = models.CharField(max_length=20, choices=status, default='new')
    order_date = models.DateTimeField(null=True)
    orderline_ids = models.ManyToManyField(SaleOrderLine, blank=True)
    amount_total = models.FloatField(blank=True)
