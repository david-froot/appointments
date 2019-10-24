from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from hygenist.models import Hygenist
from patients.models import Patient
from internal.models import Dentist, ReferredDentist, Intern
from organization.models import Organization

import stripe
stripe.api_key = settings.STRIPE_API_KEY


class User(AbstractUser):
    '''
    Custom user model
    '''
    ROLES = (('referreddentist', 'referreddentist'),
            ('organization', 'organization'), 
            ('hygenist', 'hygenist'), 
            ('dentist', 'dentist'),
            ('intern', 'intern'),
            ('patient', 'patient'))

    phone_number = models.CharField(blank=True, null=True, max_length=100)
    role = models.CharField(max_length=15, choices=ROLES, blank=True, null=True)
    address = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zipcode = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        '''
        To string 
        '''
        return '%s user: %s %s'%(self.role, self.first_name, self.last_name)


    def save(self, *args, **kwargs):
        '''
        Override save function to create related model
        '''

        super(User, self).save(*args, **kwargs)
        
        if self.role is not None:
            if self.role=='referreddentist':
                ReferredDentist.objects.get_or_create(user=self)
            if self.role=='organization':
                Organization.objects.get_or_create(user=self)
            if self.role=='hygenist':
                Hygenist.objects.get_or_create(user=self)
            if self.role=='dentist':
                Dentist.objects.get_or_create(user=self)
            if self.role=='intern':
                Intern.objects.get_or_create(user=self)
            if self.role=='patient':
                Patient.objects.get_or_create(user=self)
            
    def get_dashboard(self):
        """
        Get the URL of the dashboard for that user type
        """
        try:
            if self.is_staff:
                return '/'
            dash = getattr(self, self.role).dashboard
            return dash
        except Exception:
            print 'COULDNT GET DASHBOARD URL'
            return '/'





