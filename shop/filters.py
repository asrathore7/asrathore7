import django_filters
from .models.shops import Shop
from .models.products import Product

class ShopFilter(django_filters.FilterSet):

    class Meta:
        model = Shop
        fields = ['is_approved', 'shop_owner']

class ProductFilter(django_filters.FilterSet):

    class Meta:
        model = Product
        fields = ['product_name', 'sale_price', 'shop_id']
