from django.urls import path
from .views import UsersList, HomeView, UsersDetails, create_order, ChartData, DashboardHomeView, CustomerChartData, ShopChartData


urlpatterns = [
        path('', HomeView.as_view(template_name='home.html'), name='home'),
        path('users/shop_user_list', UsersList.as_view(), name='shopuserlist'),
        path('users/<pk>/customer_details', UsersDetails.as_view(), name='userdetails'),
        path('users/<pk>/create_order', create_order, name='createorder'),
        path('users/dashboard', DashboardHomeView.as_view(), name='dashboard'),
        path('users/dashboard_api', ChartData.as_view(), name='chart'),
        path('users/customer_dashboard_api', CustomerChartData.as_view(), name='customer_chart'),
        path('users/shop_dashboard_api', ShopChartData.as_view(), name='shop_chart'),
]
