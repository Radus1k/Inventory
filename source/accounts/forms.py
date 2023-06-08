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

class UserForm(forms.ModelForm):
    company_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }