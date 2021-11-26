from allauth.account.forms import SignupForm, LoginForm
from django import forms
# from django.db.models.enums import Choices
from .models import *

class CustomSignUpForm(SignupForm):
    USER_ROLE = (
        ('admin', 'Admin'),
        ('shop', 'Shop User'),
        ('customer', 'Customer'),
    )
    role = forms.ChoiceField(required=False, choices=USER_ROLE)

    class Meta:
        model = User
        fields = [
            'role',
        ]

    def save(self, request):
        user = super(CustomSignUpForm, self).save(request)
        user.role = self.cleaned_data['role']
        user.save()
        return user
