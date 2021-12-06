'''Urls for shop pages'''
from django.urls import path
from .views.shop_view import ShopCreateView, \
        ShopListView, ShopUpdateView, ShopDetailsView
from .views.product_view import ProductCreateView, \
        ProductListView, ProductUpdateView, \
        ProductDetailsView, ProductDeleteView


urlpatterns = [
        # Shop
        path('create_shop', ShopCreateView.as_view(), name='createshop'),
        path('shop_list', ShopListView.as_view(), name='shoplist'),
        path('<pk>/shop_edit', ShopUpdateView.as_view(), name='shopedit'),
        path('<pk>/shop_detail', ShopDetailsView.as_view(), name='shopdetail'),
        # Product
        path('<pk>/create_product', ProductCreateView.as_view(), name='createproduct'),
        path('<pk>/product_list', ProductListView.as_view(), name='productlist'),
        path('<pk>/product_edit', ProductUpdateView.as_view(), name='productedit'),
        path('<pk>/product_detail', ProductDetailsView.as_view(), name='productdetail'),
        path('<pk>/product_delete', ProductDeleteView.as_view(), name='productdelete'),
]
