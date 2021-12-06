'''Custom User's Form'''
from allauth.account.forms import SignupForm
from django import forms
from .models import User

class CustomSignUpForm(SignupForm):
    '''Add CustomSignUpForm'''
    # pylint: disable=too-few-public-methods
    USER_ROLE = (
        ('admin', 'Admin'),
        ('shop', 'Shop User'),
        ('customer', 'Customer'),
    )
    role = forms.ChoiceField(required=False, choices=USER_ROLE)

    def __str__(self):
        return self.__class__.__name__

    class Meta:
        '''Add CustomSignUpForm Meta'''
        model = User
        fields = [
            'role',
        ]

    def save(self, request):
        user = super().save(request)
        user.role = self.cleaned_data['role']
        user.save()
        return user
