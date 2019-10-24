from django import forms
from django.forms import ModelForm
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from users.models import User

class UserDetailsForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', ]


class PasswordResetForm(forms.Form):
    current_password = forms.CharField(required=True, max_length=200,label='Curent Password',
                                        widget=forms.PasswordInput(
                                        attrs={'type' : 'password','placeholder': 'Current Password'}))
    password = forms.CharField(max_length=200, required=True, 
                        label='Password',   widget=forms.TextInput(
                            attrs={'type' : 'password','placeholder': 'Password'}))

    password_confirm = forms.CharField(max_length=200, required=True, label='Retype Password',
                                       widget=forms.TextInput(attrs={
                                                    'placeholder': 'Retype Password', 
                                                    'type' : 'password'
                                        }))

    def is_valid(self):
        """
        Some custom form validation
        """
        
        # Inherited form validation function
        if not super(PasswordResetForm, self).is_valid():
            return False

        # Checl that passwords match:
        if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
            self.add_error('password', 'Passwords do not match')
            return False

        return True


class ResetPasswordForm(forms.Form):
    """
    Just get the email 
    """
    email = forms.EmailField(max_length=200, required=True)

class ConfirmPasswordReset(forms.Form):
    """
    Get the new password
    """    
    password = forms.CharField(required=True, max_length=200,widget=forms.PasswordInput)
    password_confirm = forms.CharField(required=True, max_length=200,widget=forms.PasswordInput)

    
class ChangeEmailForm(forms.Form):
    """
    Simple form to update email address
    """
    email = forms.EmailField(max_length=200, required=True)


class LoginForm(forms.Form):
    """
    For logging in
    """
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, required=True)

class SettingsForm(ModelForm):
    """
    For changing settings
    """

    class Meta:
        model = User
        fields = []


    
