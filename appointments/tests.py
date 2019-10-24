from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from models import PatientAppointmentSlot

FIXTURES = ['virtudent/fixtures/fixtures.json', ]
USER = 'patient'
PW = 'password'

class TestPages(TestCase):

    fixtures = FIXTURES

    def test_my_appointments(self):

        client = Client()
        self.assertTrue(client.login(username=USER, password=PW))
        response = client.get(reverse('appointments:myappts'))
        self.assertEquals(response.status_code, 200)

    def test_my_available_sitevisits(self):

        client = Client()
        self.assertTrue(client.login(username=USER, password=PW))
        response = client.get(reverse('appointments:visits'))
        self.assertEquals(response.status_code, 200)
        self.assertTrue('Oops' in response.content)        
        

class TestUserAppointmentRegister(TestCase):

    fixtures = FIXTURES
    
    #def test_signup(self):








