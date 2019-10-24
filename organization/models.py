from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models


class Organization(models.Model):
    '''
    An interface for company representitives
    '''
    dashboard = '/organization/dashboard/'
    user = models.OneToOneField('users.User')    
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return 'Organization %s'%self.user.username



class VisitRequest(models.Model):

    STATUS = (('Confirmed', 'Confirmed'),
              ('Rejected', 'Rejected'),
              ('Pending', 'Pending'))

    location = models.ForeignKey('appointments.Location')
    window_start = models.DateField(blank=False, null=False)
    window_end = models.DateField(blank=False, null=False)
    start = models.TimeField(verbose_name='Start Time (HH:MM)')
    end = models.TimeField(verbose_name='End Time (HH:MM)')
    details = models.TextField(max_length=1000, blank=True, null=True, 
                    verbose_name='Details (Will be shown to patients).  I.e. come to the conference room')
    status = models.CharField(max_length=100,choices=STATUS, blank=False, null=False)

    def __str__(self):
        return 'Visit Request at %s'%self.location

    #def get_absolute_url(self):
    #    return reverse('visit-details', kwargs={'pk': self.pk})
