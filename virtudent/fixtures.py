from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group
from users.models import User
from autofixture import AutoFixture


dont_add = ('group', 'user','permission', 'patient','dentist', 'referreddentist','intern','hygenist','organization')


#try:    
user = User.objects.create_user(username='patient',email=None,password='password',role='patient')
user = User.objects.create_user(username='dentist',email=None,password='password',role='dentist')
user = User.objects.create_user(username='hygenist',email=None,password='password',role='hygenist')
user = User.objects.create_user(username='intern',email=None,password='password',role='intern')
user = User.objects.create_user(username='organization',email=None,password='password', role='organization')
user = User.objects.create_user(username='referral',email=None,password='password',role='referreddentist')
user = User.objects.create_user(username='super',email=None,password='password')
user.is_superuser=True
user.is_staff=True
user.save()

#except Exception as err:
#    print err
for model in ContentType.objects.all():
    if model.model not in dont_add:
        print 'Generating models for %s'%model.model
        fixture = AutoFixture(model.model_class(), generate_fk=True)
        fixture.create(10)

