"""
Forms for the Company Representitive

DLF 2017
"""
from django import forms


class RegisterForm(forms.Form):
    """
    Register new company representitives
    """

    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, max_length=200, widget=forms.PasswordInput)
    password_confirm = forms.CharField(required=True, max_length=200, widget=forms.PasswordInput)
