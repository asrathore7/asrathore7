'''Order's page url'''
from django.urls import path
from .views import OrderDetails, OrderListView


urlpatterns = [
        path('order_details/<int:pk>', OrderDetails.as_view(), name='orderdetails'),
        path('order_list/', OrderListView.as_view(), name='orderlist'),
]
