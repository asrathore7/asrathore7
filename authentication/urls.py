from django.urls import path

from .views import UsersList


urlpatterns = [
        path('shop_user_list', UsersList.as_view(), name='shopuserlist'),
]
