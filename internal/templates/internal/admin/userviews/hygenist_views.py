from django.shortcuts import render, get_object_or_404
from portal.models import SiteVisit, PatientAppointmentSlot
from portal.views import AppointmentInfoFormView
from forms import PatientAppointmentHygenistForm, PatientAppointmentLockedHygenistForm
from users.models import User
from users.views import settings

# Create your views here.
def hygenist_dashboard(request):
    """
    The main dashboard for a hygenist
    """

    visit = SiteVisit.objects.all()[0]
    return render(request, 'hygenist/dashboard.html', {'visit' : visit})


def all_sitevisits(request):
    """
    Show all teh upcoming sitevisits for a hygenist
    """

    visits = SiteVisit.objects.all()
    return render(request, 'hygenist/sitevisittable.html', {'visits' : visits})


def sitevisit_info(request, visitid):
    """
    Show informatio about a site visit
    """

    appts = SiteVisit.objects.get(id=visitid).patientappointmentslot_set.all()
    return render(request, 'hygenist/sitevisitinfo.html', {'appts' : appts})


def patient_list(request):
    """
    Return all the patients for whom they were assigned through as ite visit
    """

    # TDO: MAKE THIS QUERY LEGIT
    slots = []
    for visit in SiteVisit.objects.all():
        slots += list(visit.patientappointmentslot_set.all())
    patients = list(set([x.patient for x in slots]))
    return render(request, 'portal/common/patients.html', {'patients' : patients})


def patient_history(request, patient_id):
    """
    Given the history of appointments for this patient
    """

    # Get the patient and all hist past appointments:
    patient = get_object_or_404(User, id=patient_id, role='patient')
    appts = PatientAppointmentSlot.objects.filter(patient=patient)

    return render(request, 'hygenist/patienthistory.html', {'appts' : appts})


class AppointmentInfoHygenistFormView(AppointmentInfoFormView):
    """
    Inherit from the appointment views
    """

    template = 'hygenist/viewappointment.html'
    form = PatientAppointmentHygenistForm
    form_locked = PatientAppointmentLockedHygenistForm
    redirect_page = '/hygenist/appointment/%s/'

    def get(self, request, apt_id):
        """
        Get object and crete the form
        """

        appt = get_object_or_404(PatientAppointmentSlot, id=apt_id, is_booked=True)
        if not appt.is_locked:
            form = self.form(initial=appt.__dict__)
        else:
            form = self.form_locked(initial=appt.__dict__)

        return render(request, self.template, {'form' :form, 'appointment' : appt})


def hygenist_settings(request):
    """
    Patient seetings page inherited from settings
    """

    return settings(request, template='hygenist/hygenistsettings.html')







