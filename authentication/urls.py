from django.urls import path

from .views import UsersList


urlpatterns = [
        path('user_list', UsersList.as_view(), name='userlist'),
]
