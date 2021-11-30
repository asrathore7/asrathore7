import django_filters
from .models import User

class UserRoleFilter(django_filters.FilterSet):

    class Meta:
        model = User
        fields = ['role']

