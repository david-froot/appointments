from django.db import models



class Hygenist(models.Model):
    '''
    Information about a hygenist
    '''

    dashboard = '/hygenist/dashboard/'
    
    user = models.OneToOneField('users.User')
    profile_photo = models.FileField(upload_to='virtudent/static/media/',blank=True, null=True)

    def __str__(self):
    	return 'Hygenist %s %s'%(self.user.first_name, self.user.last_name)


