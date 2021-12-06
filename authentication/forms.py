from allauth.account.forms import SignupForm
from django import forms
from .models import User

class CustomSignUpForm(SignupForm):
    '''Add CustomSignUpForm'''

    USER_ROLE = (
        ('admin', 'Admin'),
        ('shop', 'Shop User'),
        ('customer', 'Customer'),
    )
    role = forms.ChoiceField(required=False, choices=USER_ROLE)

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
