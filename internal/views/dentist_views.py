"""

Views for the Dentist portion of the portal 


"""
from django.shortcuts import render, get_object_or_404
from virtudent.virtlib import group_required


@group_required('dentist')
def dashboard(request):
    """
    Dashboard for the dentist
    """
    return render(request, 'internal/dentist/dashboard.html')




'''
def view_patients(request):
    """
    View thw patients that have been assigned to this dentist
    """

    context = {
        'permissions' : DentistPatientPermission.objects.filter(dentist=request.user).select_related('patient'),
        'wrapper' : 'dentist/dentistdashboardwrapper.html'
    }
    return render(request, 'portal/common/patients.html', context)

def patient_history(request, patient_id):
    """
    Given the history of appointments for this patient
    """

    # Get the patient and all hist past appointments:
    patient = get_object_or_404(User, id=patient_id, role='patient')
    appts = PatientAppointmentSlot.objects.filter(patient=patient)

    return render(request, 'hygenist/patienthistory.html', {'appts' : appts})    

'''