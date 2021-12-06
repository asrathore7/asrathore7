'''shop and product page filters'''
import django_filters
from .models.shops import Shop
from .models.products import Product

class ShopFilter(django_filters.FilterSet):
    # pylint: disable=too-few-public-methods
    '''Add Shop page filter'''
    class Meta:
        '''Add Shop page filter'''
        model = Shop
        fields = ['is_approved', 'shop_owner']

class ProductFilter(django_filters.FilterSet):
    # pylint: disable=too-few-public-methods
    '''Add Product page filter'''
    class Meta:
        '''Add Shop page filter'''
        model = Product
        fields = ['product_name', 'sale_price', 'shop_id']
