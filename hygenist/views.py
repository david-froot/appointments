"""

Views for the Hygenist portal screen 

DLF 2017

"""
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import UpdateView, CreateView, DeleteView, FormView
from appointments.models import SiteVisit, PatientAppointmentSlot
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from virtudent.virtlib import group_required
from patients.models import Patient
from models import Hygenist
from users.models import User
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from users.forms import UserDetailsForm


@group_required('hygenist')
def dashboard(request):
    """
    The main dashboard for a hygenist
    """
    upcoming = SiteVisit.objects.filter(date__gte=datetime.today())
    return render(request, 'hygenist/dashboard.html', {'upcoming' : upcoming})


@group_required('hygenist')
def my_sitevisits(request):
    """
    Show all teh upcoming sitevisits for a hygenist
    """
    visits = SiteVisit.objects.all().order_by('-date')
    return render(request, 'hygenist/my_sitevisits.html', {'visits' : visits})


@group_required('hygenist')
def sitevisit_details(request, pk):
    """
    Show informatio about a site visit
    """
    appts = SiteVisit.objects.get(id=pk).patientappointmentslot_set.all()
    return render(request, 'hygenist/sitevisit_details.html', {'appts' : appts})


@group_required('hygenist')
def patient_list(request):
    """
    Return all the patients for whom they were assigned through as ite visit
    # TDO: MAKE THIS QUERY LEGIT
    """
    slots = []
    for visit in SiteVisit.objects.all():
        slots += list(visit.patientappointmentslot_set.all())
    patients = list(set([x.patient for x in slots]))
    return render(request, 'hygenist/patient_list.html', {'patients' : patients})


@group_required('hygenist')
def patient_history(request, patient_id):
    """
    Given the history of appointments for this patient
    """
    patient = get_object_or_404(Patient, id=patient_id)
    appts = PatientAppointmentSlot.objects.filter(patient=patient)

    return render(request, 'hygenist/patient_history.html', {'appts' : appts})


@method_decorator(group_required('hygenist'), name='dispatch')
class SettingsView(UpdateView):
    """
    Return user settings
    """

    model = User
    fields = ['first_name', 'last_name', 'email', 'phone_number', 
            'address', 'city', 'state', 'zipcode']
    template_name = 'hygenist/settings.html'
    success_url = '/hygenist/dashboard/'

    def get_object(self, *args):
        return User.objects.get(id=self.request.user.id)


@method_decorator(group_required('hygenist'), name='dispatch')
class ProfilePhotoView(UpdateView):
    """
    Patient seetings page inherited from settings
    """
    template_name = 'hygenist/profilephoto_form.html'
    fields = ['profile_photo', ]
    model = Hygenist
    success_url = '/hygenist/dashboard/'

    def get_object(self, *args):
        return Hygenist.objects.get(id=self.request.user.hygenist.id)


@method_decorator(group_required('hygenist'), name='dispatch')
class AppointmentInfoHygenistFormView(UpdateView):

    model = PatientAppointmentSlot
    template_name = 'hygenist/appointment_details.html'
    fields = ['notes', 'upload1', 'is_noshow', 'is_locked', 'referred_dentist']
    context_object_name = 'appointment'

    def get_success_url(self):
        print self.object.sitevisit.id
        return reverse('visitinfo', kwargs={'pk':self.object.sitevisit.id}) 



'''

def toggle_setting(request, apt_id):
    """
    Toggle different patient boolean fields
    """

    attr = request.GET.get('attr', None)
    if attr not in ('is_paid', 'reimbursement_confirmed',
                    'billing_recieved', 'billing_sent','is_break'):
        return Http404
    
    visit = get_object_or_404(PatientAppointmentSlot, id=apt_id)
    
    # Invert the attribute:
    setattr(visit, attr, not getattr(visit, attr))
    visit.save()    

    return HttpResponse('Success')

'''

