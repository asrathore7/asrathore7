'''User's Page filters'''
import django_filters
from .models import User

class UserRoleFilter(django_filters.FilterSet):
    '''UserRoleFilter filters'''
    class Meta:
        '''UserRoleFilter Meta filters'''
        model = User
        fields = ['role']

