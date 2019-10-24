"""

Views only for patients

DLF 2017

"""
from django.views.generic.edit import UpdateView, CreateView, DeleteView, FormView
from appointments.models import PatientAppointmentSlot
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from virtudent.virtlib import group_required
from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login, logout
from users.models import User
from models import *
from forms import *


class RegisterPatient(FormView):
    """
    Register new patients
    """
    template_name = 'users/form.html'
    success_url = '/patients/dashboard/'
    form_class = RegisterPatientForm

    def form_valid(self, form):
        user = User.objects.create_user(form.cleaned_data['email'],
                                    form.cleaned_data['email'],
                                    form.cleaned_data['password'],
                                    role='patient')
        login(self.request, user)
        return super(RegisterPatient, self).form_valid(form)


#@group_required('patient')
def dashboard(request):
    """
    The portal homepage
    """
    return render(request, 'patients/dashboard.html')


#@group_required('patient')
def myhealth(request):
    """
    The patients health records
    """
    slots = PatientAppointmentSlot.objects.filter(patient=request.user.patient)
    return render(request, 'patients/myhealth.html', {'slots' : slots.order_by('start')})

#@group_required('patient')
def settings(request):
    """
    Settings for a particular user
    """
    return render(request, 'patients/settings.html')


#@group_required('patient')
def update_payment(request):
    """
    Update payment information
    """
    return render(request, 'patients/paymentinfo_update.html')


#@group_required('patient')
def form_overview(request):
    """
    Overview of the forms the patient needs to fill out
    """
    return render(request, 'patients/formsummary.html')


#@method_decorator(group_required('patient'), name='dispatch')
class PatientInformationView(UpdateView):
    """
    Set patient information
    """
    model = PatientInformation
    form_class = PatientInformationForm
    template_name='patients/medications.html'
    success_url = '/patients/forms/'

    def get_object(self, queryset=None):
        try:
            return self.model.objects.get(patient=self.request.user.patient)
        except ObjectDoesNotExist:
            return self.model()

    def form_valid(self, form):
        form.instance.patient = self.request.user.patient
        return super(PatientInformationView, self).form_valid(form)


#@method_decorator(group_required('patient'), name='dispatch')
class MedicineFormView(CreateView):
    """
    Medications lista nd update:
    """
    model = Medication
    form_class = MedicationForm
    template_name = 'patients/medications.html'
    success_url = '/patients/forms/'

    def get_context_data(self, **kwargs):
        context = super(MedicineFormView, self).get_context_data(**kwargs)
        context['existing'] = self.model.objects.filter(patient=self.request.user.patient)
        
        return context

    def form_valid(self, form):
        form.instance.patient = self.request.user.patient
        return super(MedicineFormView, self).form_valid(form)


#@method_decorator(group_required('patient'), name='dispatch')
class MedicineDeleteView(DeleteView):
    """
    Delete medications
    """
    model = Medication
    success_url = '/patients/forms/'

    def get_object(self, queyset=None):
        return self.model.objects.get(id=self.kwargs['pk'], patient=self.request.user.patient)


#@method_decorator(group_required('patient'), name='dispatch')
class AllergyFormView(MedicineFormView):
    """
    Create Allergy records for a patient
    """
    form_class = AllergyForm
    model = Allergy
    success_url = '/patients/forms/allergy/'
    template_name = 'patients/allergies.html'

#@method_decorator(group_required('patient'), name='dispatch')
class AllergyDeleteView(MedicineDeleteView):
    """
    Delete allergy forms
    """
    model = Allergy
    success_url = '/patients/forms/allergy/'


#@method_decorator(group_required('patient'), name='dispatch')
class SurgeryFormView(MedicineFormView):
    """
    Create Surgeries for a patient
    """
    form_class = SurgeryForm
    model = Surgery
    success_url = '/patients/forms/surgery/'
    template_name = 'patients/surgeries.html'


#@method_decorator(group_required('patient'), name='dispatch')
class SurgeryDeleteView(MedicineDeleteView):
    """
    Delete surgery record
    """
    model = Surgery
    success_url = '/patients/forms/surgery/'


#@method_decorator(group_required('patient'), name='dispatch')
class FamilyHistoryFormView(MedicineFormView):
    """
    Family History record for aptient
    """
    form_class = FamilyHistoryForm
    model = FamilyHistory
    success_url = '/patients/forms/familyhistory/'
    template_name = 'patients/famhistory.html'


#@method_decorator(group_required('patient'), name='dispatch')
class FamilyHistoryDeleteView(MedicineDeleteView):
    """
    Delete family history forms
    """
    model = FamilyHistory
    success_url = '/patients/forms/familyhistory/'


#@method_decorator(group_required('patient'), name='dispatch')
class HealthHistoryFormView(PatientInformationView):
    """
    Health History record for patient
    """

    form_class = HealthHistoryForm
    model = HealthHistory
    success_url = '/patients/forms/'
    template_name = 'patients/healthhistory.html'


#@method_decorator(group_required('patient'), name='dispatch')
class HealthHistoryDeleteView(MedicineDeleteView):
    """
    Delete health history 
    """
    model = HealthHistory
    success_url = '/patients/forms/healthhistory/'
