"""
Models for Appointments app 


DLF 2017
"""
from __future__ import unicode_literals
from django.db import models
from django.db.models import Q
from datetime import datetime, timedelta
from django.core.urlresolvers import reverse, reverse_lazy
from datetime import datetime, timedelta
from users.models import Organization


class Insurer(models.Model):
    """
    For approved insruance entities
    """

    insurer_name = models.CharField(max_length=1000, blank=False, null=False, unique=True, verbose_name='Insurer Name')
    insurer_code = models.CharField(max_length=1000, blank=False, null=False, unique=True, verbose_name='Insurer Code') 
    copay = models.FloatField(default=0, verbose_name='Co-Pay For Patients')
    address = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Address')
    city = models.CharField(max_length=1000, blank=True, null=True, verbose_name='City')
    state = models.CharField(max_length=2, blank=True, null=True, verbose_name='State')
    zipcode = models.CharField(max_length=7, blank=True, null=True, verbose_name='Zip Code')
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Description')

    def __str__(self):
        return 'Insurer: %s'%self.insurer_name


class Location(models.Model):
    """
    The specifics of a location
    """

    organization = models.ForeignKey('organization.Organization', blank=False, null=False)
    name = models.CharField(max_length=100, blank=False, null=False, verbose_name='Location Name')
    address = models.CharField(max_length=100, blank=False, null=False, verbose_name='Address')
    city = models.CharField(max_length=100, blank=False, null=False, verbose_name='City')
    state = models.CharField(max_length=2, blank=False, null=False, verbose_name='State')
    zipcode = models.CharField(max_length=7, blank=False, null=False, verbose_name='Zip Code')

    def __str__(self):
        return self.name


class SiteVisit(models.Model):
    """
    A record of the dates that a dentist will be onsite
    """

    date = models.DateField(blank=False, verbose_name='Date')
    location = models.ForeignKey(Location, blank=False, null=False, db_index=True)    
    
    hygenist = models.ForeignKey('hygenist.Hygenist', verbose_name='On-Site Hygenist',blank=True, null=True)
    start = models.TimeField(verbose_name='Start Time (HH:MM)')
    end = models.TimeField(verbose_name='End Time (HH:MM)')
    duration = models.IntegerField(verbose_name='Duration (Minutes)')
    details = models.TextField(max_length=300, blank=True, null=True, 
                    verbose_name='Details (Will be shown to patients)  i.e. come to the conference room')
    is_confirmed = models.BooleanField(default=True)

    rating = models.IntegerField(blank=True, null=True, default=None)
    feedback = models.TextField(verbose_name='Additional Feedback',blank=True, null=True, default=None)


    def __str__(self):
        return 'Site Visit to %s'%(self.location)

    class Meta:
        
        unique_together = ('location', 'date', 'hygenist')

    def num_booked(self):
        """
        return how many of the slots are booked
        """
        return self.patientappointmentslot_set.filter(is_booked=True).count()
    
    def total_slots(self):
        """
        Return how many slots there are total
        """
        return self.patientappointmentslot_set.count()

    def total_free(self):
        """
        Return how many slots remain
        """
        return self.patientappointmentslot_set.filter(is_booked=False).count()

    def save(self, *args, **kwargs):
        """
        Override the save method to create site visits
        """
        super(SiteVisit, self).save(*args, **kwargs)

        obj = SiteVisit.objects.get(id=self.id)
        start = datetime.combine(obj.date, obj.start)
        time_df = timedelta(minutes=abs(obj.duration))

        while start + time_df <= datetime.combine(obj.date, obj.end):
            PatientAppointmentSlot.objects.get_or_create(sitevisit=obj, start=start, end=start+time_df)
            start += time_df

        
        
        
class PatientAppointmentSlot(models.Model):
    """
    A patients appointment
    """

    sitevisit = models.ForeignKey(SiteVisit)
    patient = models.ForeignKey('patients.Patient', default=None, null=True, blank=True,
                                related_name='patient', verbose_name='Patient')
    referred_dentist = models.ForeignKey('internal.ReferredDentist', blank=True, null=True, 
                                                            verbose_name='Refer to Dentist')
    is_booked = models.BooleanField(default=False, verbose_name='Is Booked')
    is_break = models.BooleanField(default=False, verbose_name='Is Break')
    start = models.DateTimeField(verbose_name='Start Time')
    end = models.DateTimeField(verbose_name='End Time')
    is_paid = models.BooleanField(default=False, verbose_name='Paid')
    amount = models.FloatField(default=0, verbose_name='Amount')
    reimbursement_confirmed = models.BooleanField(default=False, verbose_name='Insurance Reimbursement Confirmed')
    notes = models.TextField(max_length=10000, blank=True, null=True, verbose_name='Notes')
    billing_sent = models.BooleanField(default=False, verbose_name='Billing Sent to Insurer')
    billing_recieved = models.BooleanField(default=False, verbose_name='Billing Recieved From Insurer')
    is_noshow = models.BooleanField(default=False, verbose_name='No Show') 
    #last_notification = models.DateTimeField(default=datetime(2010,1,1))

    # File fields:
    upload1 = models.FileField(blank=True, null=True, verbose_name='File 1')
    upload2 = models.FileField(blank=True, null=True, verbose_name='File 2')
    upload3 = models.FileField(blank=True, null=True, verbose_name='File 3')#upload_to='not_required'
    addendum_upload1 = models.FileField(blank=True, null=True, verbose_name='Addendum File 1')
    addendum_upload2 = models.FileField(blank=True, null=True, verbose_name='Addendum File 2')
    addendum_upload3 = models.FileField(blank=True, null=True, verbose_name='Addendum File 3')#upload_to='not_required'

    # Locking ability:
    is_locked = models.BooleanField(default=False, verbose_name='Locked', 
                    help_text='WARNING: Once you have locekd an appointment you cannot modify it')
    lock_timestamp = models.DateTimeField(blank=True, null=True, verbose_name='Time Locked')
    addendum_notes = models.TextField(max_length=10000, blank=True, null=True, verbose_name='Addendum Notes')

    class Meta:
        unique_together = ('sitevisit', 'start')

    def __str__(self):
        return 'Patient Appointment: %s->%s'%(self.start, self.end)

    def get_absolute_url(self):
        return reverse('internal:h-appt', kwargs={'pk': self.pk})

    def book(self, patient, save=False):
        """
        Book an appointment
        """

        if self.is_booked or self.is_break:
            raise ValueError

        self.is_paid = True
        self.is_booked = True
        self.is_break = False
        self.patient = patient
        self.amount = patient.info.insurer.copay

        if save:
            self.save()

    def unbook(self, save=False):
        """
        Unbook an appointment
        """

        self.is_paid = False
        self.is_booked = False
        self.patient = None
        
        if save:
            self.save()

    def can_cancel(self):
        return self.sitevisit.date - datetime.now().date() < timedelta(days=7)

    




