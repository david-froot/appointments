from django.test import TestCase, Client
from users.models import User


FIXTURES = ['virtudent/fixtures/fixtures.json']
USER = 'patient'
PW = 'password'

class TestGetPages(TestCase):

    fixtures = FIXTURES

    def test_get_login(self):

        client = Client()
        response = client.get('/users/login/')
        self.assertEquals(response.status_code, 200)


    def test_get_logout(self):

        client = Client()
        response = client.get('/users/logout/')
        self.assertEquals(response.status_code, 302)


    def test_get_changepassword(self):

        client = Client()
        client.login(username=USER, password=PW)
        response = client.get('/users/settings/')
        self.assertEquals(response.status_code, 200)


    def test_changepw(self):
        client = Client()
        client.login(username=USER, password=PW)
        response = client.post('/users/changepassword/', {
                    'password' : PW, 
                    'password_confirm' : PW, 
                    'current_password': PW,
                })
        self.assertTrue('Success' in response.content)

    def test_get_changeemail(self):
        client = Client()
        client.login(username=USER, password=PW)
        response = client.get('/users/changeemail/')
        self.assertEquals(response.status_code, 200)



