# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User

class SignUpForm(UserCreationForm):
    company_name = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ('username', 'company_name', 'email', 'password1', 'password2', 'phone_number')
