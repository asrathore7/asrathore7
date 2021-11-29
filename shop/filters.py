import django_filters
from .models.shops import Shop

class ShopFilter(django_filters.FilterSet):

    class Meta:
        model = Shop
        fields = ['is_approved', 'shop_owner']
