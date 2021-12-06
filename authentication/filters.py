'''User's Page filters'''
import django_filters
from .models import User

class UserRoleFilter(django_filters.FilterSet):
     # pylint: disable=too-few-public-methods
    '''UserRoleFilter filters'''
    class Meta:
        '''UserRoleFilter Meta filters'''
        model = User
        fields = ['role']
