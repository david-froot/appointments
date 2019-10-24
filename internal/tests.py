from django.test import TestCase, Client
from django.core.urlresolvers import reverse

FIXTURES = ['virtudent/fixtures/fixtures.json', ]

class TestHygenistViews(TestCase):

    fixtures = FIXTURES

    def test_dashboard(self):

        client = Client()
        self.assertTrue(client.login(username='hygenist', password='password'))

        response = client.get(reverse('internal:d-dashboard'))
        self.assertEquals(response.status_code, 200)
