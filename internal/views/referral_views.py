"""

Views for the Dentist referral portal screen 

DLF 2017

"""
from patients.models import Patient
from appointments.models import PatientAppointmentSlot
from django.shortcuts import render, get_object_or_404, redirect

def dashboard(request):
    '''
    Dashboard for referred dentists to get information
    '''
    return render(request, 'internal/referral/dashboard.html')


def patients(request):
    '''
    Show all the patients that where assigned to this referred dentist
    '''

    patients = PatientAppointmentSlot.objects.filter(
            referred_dentist=request.user.referreddentist).select_related('patient')
    patients = list(set([ x.patient for x in patients]))
    template = 'internal/referral/patient_list.html'
    
    return render(request, template, {'patients': patients})
    

def patient_history(request, id):
    """
    Get history of a given patient
    """
    patient = get_object_or_404(Patient, id=id)
    appts = PatientAppointmentSlot.objects.filter(patient=patient)
    template = 'internal/referral/patient_history.html'

    return render(request, template, {'appts' : appts})


def appointment_details(request, id):
    """
    Details about an appointment
    """

    appt = get_object_or_404(PatientAppointmentSlot, id=id)
    template = 'internal/referral/appointment_details.html'

    return render(request, template,{'appt': appt})
