"""
David Froot

Virtudent 

Appointments views for users
"""
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.core.exceptions import ObjectDoesNotExist
from models import PatientAppointmentSlot, SiteVisit
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta
from forms import *
import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_API_KEY


def my_appointments(request):
    """
    The patients schedule
    """
    apt = PatientAppointmentSlot.objects.filter(patient=request.user.patient)
    return render(request, 'appointments/myappointments.html', {'appt' : apt})
    

def view_my_sitevisits(request):
    """
    View all the site visits for a given user
    """
    try:
        visits = SiteVisit.objects.filter(location__organization=request.user.patient.info.company)
    except ObjectDoesNotExist:
        return render(request, 'appointments/oops.html')
    
    return render(request, 'appointments/mysitevisits.html', {'visits' : visits})



def confirm_appointment(request, slot_id):
    """
    Show the customre a confirmation page
    """
    context = {
        'slot' :  get_object_or_404(PatientAppointmentSlot, id=slot_id, is_booked=False),
        'needToPay' : request.user.patient.info.insurer.copay - request.user.patient.credit,
        'cust'   : request.user.patient.get_customer()
    }
    return render(request, 'appointments/bookingconfirm.html', context)



def confirm_pay_appointment(request, slot_id):
    """
    Pay and book the appointment
    """
    slot = get_object_or_404(PatientAppointmentSlot, pk=slot_id)
    if PatientAppointmentSlot.objects.filter(sitevisit=slot.sitevisit, 
                            patient=request.user.patient).count() > 0:
        return redirect('/')
        
    amount = request.user.patient.info.insurer.copay 
    credit_applied = min(amount, request.user.patient.credit)
    balance_remaining = amount - credit_applied

    # If no need to pay, just confirm the booking
    if balance_remaining <= 0:
        slot.book(request.user.patient, save=True)
        request.user.patient.credit -= credit_applied
        request.user.patient.save()
        return redirect(reverse('appointments:myappts'))

    # Charge the card and record the transaciton if successful:
    try:  
        customer = request.user.patient.get_customer(stripe_token=request.POST.get('stripeToken'))
        stripe.Charge.create(amount=int(balance_remaining*100), currency="usd", customer=customer.id)
        slot.book(request.user.patient, save=True)

    except stripe.error.CardError:
        return Http404

    return redirect(reverse('appointments:myappts'))



def cancel_appointment(request, slot_id):
    """
    Cancel a patients appointment if they are allowed, and credit the account
    """
    slot = get_object_or_404(PatientAppointmentSlot, id=slot_id, patient=request.user.patient)
    if slot.is_paid and slot.can_cancel():
        request.user.patient.credit += slot.amount
        request.user.patient.save()

    slot.unbook(save=True)
    return redirect(reverse('appointments:myappts'))




