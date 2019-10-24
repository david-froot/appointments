"""
David Froot 

forms for patients models

"""

from django import forms
from django.forms import ModelForm, formset_factory
from users.models import User
from patients.models import *


class RegisterPatientForm(forms.Form):
    """
    Form for registering users
    """

    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, max_length=200, widget=forms.PasswordInput)
    password_confirm = forms.CharField(required=True, max_length=200, widget=forms.PasswordInput)

    
    def is_valid(self):
        """
        Custom form validation for registering users
        """
        valid = super(RegisterPatientForm, self).is_valid()
        
        # Check the initial validity:
        if not valid:
            return valid

        # Verify the passwords match:
        if not self.cleaned_data['password'] == self.cleaned_data['password_confirm']:
            self.add_error('password', 'Passwords do not match')
            valid = False

        if User.objects.filter(email=self.cleaned_data['email']).exists():
            self.add_error('email', 'Email is already in use')    
            valid = False

        return valid



class PatientInformationForm(ModelForm):
    """
    Patient PatientInformationForm
    """
    
    class Meta:
        model = PatientInformation
        exclude = ['patient']


class MedicationForm(ModelForm):
    """
    For getting patient medications
    """

    class Meta:
        model = Medication
        exclude = ['patient']
        

class AllergyForm(ModelForm):
    """
    For getting patient allergy
    """

    class Meta:
        model = Allergy
        exclude = ['patient']


class SurgeryForm(ModelForm):
    """
    For getting patient allergy
    """

    class Meta:
        model = Surgery
        exclude = ['patient']


class FamilyHistoryForm(ModelForm):
    """
    For getting patient allergy
    """
    
    class Meta:
        model = FamilyHistory
        exclude = ['patient']


class HealthHistoryForm(ModelForm):
    """
    Seperate form for health histor
    """

    class Meta:
        model = HealthHistory
        exclude = ['patient']

