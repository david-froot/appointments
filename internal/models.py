from django.db import models

class ReferredDentist(models.Model):
    '''
    A one to one for users who are referred dentists
    '''

    dashboard = '/internal/dentist/dashboard/'
    user = models.OneToOneField('users.User')

    def __str__(self):
        return 'Dentist Referral %s %s'%(self.first_name, self.last_name)
        


class Dentist(models.Model):
    '''
    Information about dentists who are on the platform
    '''

    dashboard = '/internal/dentist/dashboard/'
    user = models.OneToOneField('users.User')


class Intern(models.Model):
    '''
    Interns or low level workers with minimum permissions
    '''

    dashboard = '/internal/dentist/dashboard/'
    user = models.OneToOneField('users.User')


