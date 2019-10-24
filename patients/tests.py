from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from users.models import User


USER = 'patient'
PW = 'password'

class OnboardingTestCase(TestCase):


    def form_tester(self, data, keyword, url, context_var):

        # Log in the client:
        User.objects.create_user(username=USER, password=PW, role='patient')
        client = Client()
    
        self.assertTrue(client.login(username=USER, password=PW))

        response = client.get(reverse('patients:forms'))
        

        client.post(url, data)
        response = client.get(url)

        self.assertEquals(response.status_code, 200)
        #self.assertTrue(keyword in response.content)
    
        # Test the main page context variable:
        response = client.get(reverse('patients:forms'))
        self.assertEquals(response.status_code, 200)
        


    def test_register_patient(self):

        client = Client()
        response = client.get(reverse('patients:register'))
        self.assertEquals(response.status_code, 200)

        response = client.post('/patients/register/', { 
                        'email' : 't@g.co',
                        'password' : 'pw',
                        'password_confirm' : 'pw'
                    })
        self.assertEquals(response.status_code, 302)
        self.assertTrue(client.login(username='t@g.co', password='pw'))


    def test_health_information(self):

        data =  {
                u'last_name': u'Name', 
                u'relationship': u'F', 
                u'insurer': u'1', 
                u'company': u'1', 
                u'policyholder_gender': u'Male', 
                u'policyholder_address': u'', 
                u'alternative_phone': u'9783943012', 
                u'contact_email': u'dfroot@mba2017.hbs.edu', 
                u'contact_first_name': u'A', 
                u'address': u'123 Fake Street', 
                u'contact_alternative_phone': u'9783943012', 
                u'policyholder_last_name': u'Blah', 
                u'insurance_policy_number': u'234', 
                u'city': u'Boston', 
                u'first_name': u'My', 
                u'policy_relationship': u'Self', 
                u'contact_last_name': u'B', 
                u'phone': u'9783943012', 
                u'dob': u'10/16/1989', 
                u'gender': 
                u'Male', 
                u'zipcode': u'02139', 
                u'policyholder_dob': u'10/26/1989', 
                u'policyholder_employer': u'', 
                u'state': u'MA', 
                u'policyholder_fist_name': u'Blah', 
                u'contact_phone': u'9783943012', 
                u'insurance_group_number': u'1224'
        }
        self.form_tester(data, '9783943012', reverse('patients:info'), 'form')


    def test_health_history(self):
        data = {
                'is_additional_conerns': '', 
                'primary_care_physician': 'PCPAAAA', 
                'hours_per_day': '',
                'last_visit': '',
                'is_kidney_disease': 'on',
            }
        self.form_tester(data, 'PCPAAAA', reverse('patients:healthhistory'), 'healthhist')


    def test_medications(self):
        data = { 
                'strength': '89mg', 
                'date_started': '10/16/1989', 
                'medication_name': 'Ambien',
                'dosage_form': 'Pill'
            }
        self.form_tester(data, 'Ambien', reverse('patients:medicine'), 'meds')


    def test_family_history(self):
        data = {
                'status': 'None', 
                'disease': 'Heart Disease',
                'relationship': 'Father', 
                'details': 'Somedetail',
            }
        self.form_tester(data, 'Disease', reverse('patients:familyhistory'), 'famhist')
        

    def test_surgeries(self):
        data = {
                u'date': u'10/10/2009', 
                u'procedure_name': u'BSurg',
                u'surgeon_name': u'SSSSS'
            }
        #self.form_tester(data, 'BSurg', reverse('patients:surgery'), 'surgery')
        

    def test_allergies(self):
        data = {
            'allergen_type': 'Other', 
            'allergen_name': 'Pollen', 
            'severity': '1', 
            'reaction': 'Nose',
        }
        self.form_tester(data, 'Pollen', reverse('patients:allergy'), 'allergy')
        






class TestDashboard(TestCase):

    

    def test_view(self, url=reverse('patients:dashboard')):
        client = Client()
        User.objects.create_user(username=USER,password=PW,role='patient')
        self.assertTrue(client.login(username=USER, password=PW))
        response = client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_settings(self):
        self.test_view(url=reverse('patients:settings'))

    def test_forms_home(self):
        self.test_view(url=reverse('patients:forms'))

    def test_forms_patientinfo(self):
        self.test_view(url=reverse('patients:info'))

    def test_forms_medicine(self):
        self.test_view(url=reverse('patients:medicine'))

    def test_forms_surgery(self):
        self.test_view(url=reverse('patients:surgery'))
    
    def test_forms_allergy(self):
        self.test_view(url=reverse('patients:allergy'))

    def test_forms_familyhistory(self):
        self.test_view(url=reverse('patients:familyhistory'))

    def test_forms_healthhistory(self):
        self.test_view(url=reverse('patients:healthhistory'))






