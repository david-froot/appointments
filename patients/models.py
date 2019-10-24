"""
David Froot

Models for the patient module
"""
from __future__ import unicode_literals
from django.db import models
import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_API_KEY


GENDER = (('Male', 'Male'),
          ('Female', 'Female'),
          ('Other', 'Other'))

HOLDER = (('Self', 'Self'),
          ('Other', 'Other'))

HILO = (('High', 'High'),
        ('Low', 'Low'))

ALLERGEN_TYPE = (('Drug', 'Drug'),
                 ('Other', 'Other'))

STATUS = (('Active', 'Active'),
          ('Inactive', 'Inactive'))


class Patient(models.Model):
    '''
    A patient user role
    '''

    dashboard = '/patients/dashboard/'
    user = models.OneToOneField('users.User')
    stripe_customer_id = models.CharField(max_length=150, blank=True, null=True, default=None)
    credit = models.FloatField(default=0)
    

    def get_customer(self, stripe_token=None):

        if self.stripe_customer_id is not None:
                return stripe.Customer.retrieve(self.stripe_customer_id)

        if stripe_token is not None:
            customer = stripe.Customer.create(source=stripe_token)
            self.stripe_customer_id = customer.id
            self.save()
            return customer
        
        return {}
        

class PatientInformation(models.Model):
    """
    Basic data about the patient
    """

    patient = models.OneToOneField(Patient, primary_key=True, related_name='info')

    first_name = models.CharField(max_length=1000, blank=False, null=False, verbose_name='First Name')
    last_name = models.CharField(max_length=1000, blank=False, null=False, verbose_name='Last Name')
    company = models.ForeignKey('organization.Organization', verbose_name='Name of Company')
    insurer = models.ForeignKey('appointments.Insurer', verbose_name='Name of Insurer')
    insurance_policy_number = models.CharField(max_length=100, blank=False, null=False, 
                                                verbose_name='Insurance Policy Number')
    insurance_group_number = models.CharField(max_length=100, blank=False, null=False, 
                                                verbose_name='Insurance Group Number')

    address = models.CharField(max_length=1000, blank=False, null=False, verbose_name='Address')
    city = models.CharField(max_length=1000, blank=False, null=False, verbose_name='City')
    state = models.CharField(max_length=2, blank=False, null=False, verbose_name='State')
    zipcode = models.CharField(max_length=7, blank=False, null=False, verbose_name='Zip Code')
    gender = models.CharField(max_length=6, blank=False, null=False, choices=GENDER, verbose_name='Gender')
    dob = models.DateField(blank=False, null=False, verbose_name='Date of Birth (MM/DD/YYYY)')
    phone = models.CharField(max_length=20, blank=False, null=False, verbose_name='Phone Number')
    alternative_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Alternative Phone')

    # Emergency Contact:
    contact_first_name = models.CharField(max_length=1000, blank=False, null=False, 
                                            verbose_name='Emergency Contact First Name')
    contact_last_name = models.CharField(max_length=1000, blank=False, null=False, 
                                            verbose_name='Emergency Contact Last Name')
    relationship = models.CharField(max_length=1000, blank=False, null=False, 
                                            verbose_name='Relationship')
    contact_phone = models.CharField(max_length=1000, blank=False, null=False, 
                                            verbose_name='Emergency Contact Phone Number')
    contact_alternative_phone = models.CharField(max_length=1000, blank=True, null=True, 
                                            verbose_name='Emergency Contact Alternative Phone')
    contact_email = models.EmailField(blank=False, null=False, verbose_name='Emergency Contact Email Address')


    # Relationship to policyholder:
    policy_relationship = models.CharField(max_length=1000, blank=True, null=True, choices=HOLDER, 
                                            verbose_name='Relationship to Policy Holder')
    policyholder_fist_name = models.CharField(max_length=1000, blank=True, null=True, 
                                            verbose_name='If Other, Policy Holder First Name')
    policyholder_last_name = models.CharField(max_length=1000, blank=True, null=True, 
                                            verbose_name='If Other, Policy Holder Last Name`')
    policyholder_gender = models.CharField(max_length=10, blank=True, null=True, choices=GENDER, 
                                            verbose_name='If Other, Policy Holder Gender')
    policyholder_dob = models.DateField(blank=True, null=True, 
                                            verbose_name='If Other, Policy Holder Date of Birth (MM/DD/YYYY)')
    policyholder_employer = models.CharField(max_length=1000, blank=True, null=True, 
                                            verbose_name='If Other, Policy Holder Employers')
    policyholder_address = models.CharField(max_length=1000, blank=True, null=True, 
                                            verbose_name='If Other, Policy Holder Address')

    def __str__(self):
        '''
        Custom to string
        '''
        return 'Patient Info %s %s'%(self.first_name, self.last_name)


class HealthHistory(models.Model):
    """
    A health history set
    """

    patient = models.OneToOneField(Patient, primary_key=True)

    # General history:
    primary_care_physician = models.CharField(max_length=1000, blank=True, null=True, 
                                            verbose_name='Primary Care Physician')
    last_visit = models.DateField(blank=True, null=True, verbose_name='Date of last visit (MM/DD/YYY)')
    is_work_at_computer = models.BooleanField(default=False, verbose_name='Do you work at a computer?')
    hours_per_day = models.FloatField(blank=True, null=True, verbose_name='If yes, how many hours per day?')

    # Health histroy:
    is_kidney_disease = models.BooleanField(default=False, verbose_name='Kidney Disease')
    is_venereal_disease = models.BooleanField(default=False, verbose_name='Venereal Disease')
    is_diabetes = models.BooleanField(default=False, verbose_name='Diabetes')
    is_thyroid_problems = models.BooleanField(default=False, verbose_name='Thyroid Problems')
    is_skin_disease = models.BooleanField(default=False, verbose_name='Skin Disease')
    is_eyeProblems = models.BooleanField(default=False, verbose_name='Eye Problems')
    is_arthritis = models.BooleanField(default=False, verbose_name='Arthritis')
    is_epilepsy = models.BooleanField(default=False, verbose_name='Epilepsy')
    is_nervous_disorders = models.BooleanField(default=False, verbose_name='Nervous Disorders')
    is_mental_illness = models.BooleanField(default=False, verbose_name='Mental Illness')
    is_frequent_headaches = models.BooleanField(default=False, verbose_name='Frequency Headaches')
    is_earaches = models.BooleanField(default=False, verbose_name='Ear Aches')
    is_hay_fever = models.BooleanField(default=False, verbose_name='Hay Fever')
    is_asthma = models.BooleanField(default=False, verbose_name='Asthma')
    is_sleep_apnea = models.BooleanField(default=False, verbose_name='Sleep Apnea')
    is_tumor_treatment = models.BooleanField(default=False, verbose_name='Tumor Treatment')
    is_hivaids = models.BooleanField(default=False, verbose_name='HIV / AIDS')
    is_aids_Virus_carrier = models.BooleanField(default=False, verbose_name='AIDS Virus Carrier')
    is_joints_hip_replacement = models.BooleanField(default=False, verbose_name='Hip Joint Replacement')
    is_recent_change_weight = models.BooleanField(default=False, verbose_name='Recent Weight Change')
    is_pregnant = models.BooleanField(default=False, verbose_name='Pregnant')
    is_birth_control_pill = models.BooleanField(default=False, verbose_name='Birth Control Pills')
    is_premedications = models.BooleanField(default=False, verbose_name='Premedications')
    is_rheumatismal_fever = models.BooleanField(default=False, verbose_name='Rheumatismal Fever')
    is_fever = models.BooleanField(default=False, verbose_name='Fever')
    is_bleeding = models.BooleanField(default=False, verbose_name='Bleeding')
    is_anemia = models.BooleanField(default=False, verbose_name='Anemia')
    is_osteoporosis = models.BooleanField(default=False, verbose_name='Osteoporosis')
    #is_bloodpressureHistory = models.BooleanField(default=False, choices=HILO, verbose_name='Bloodpressure History')
    is_frequentColds = models.BooleanField(default=False, verbose_name='Frequent Colds')
    is_frequent_sinusitis = models.BooleanField(default=False, verbose_name='Frequent Sinusitis')
    is_lungProblems = models.BooleanField(default=False, verbose_name='Lung Problems')
    is_tuberculosis = models.BooleanField(default=False, verbose_name='Tuberculosis')
    is_digestive_problems = models.BooleanField(default=False, verbose_name='Digestive Problems')
    is_stomach_ulcers = models.BooleanField(default=False, verbose_name='Stomach Ulcers')
    is_liver_disease = models.BooleanField(default=False, verbose_name='Liver Disease')
    is_hepatitis = models.BooleanField(default=False, verbose_name='Hepatisis')
    is_dental_fear = models.BooleanField(default=False, verbose_name='Fear of Dental Treatment')
    is_additional_conerns = models.TextField(max_length=1000, blank=True, null=True, verbose_name='Additional Concerns')

    #Social history
    is_smoker = models.BooleanField(default=False, verbose_name='Do you smoke?')
    is_drinker = models.BooleanField(default=False, verbose_name='Do you drink alcohol?')

    def __str__(self):
        return 'Health History for %s %s'%(self.patient.first_name, self.patient.last_name)


class Medication(models.Model):
    """
    Medications
    """

    patient = models.ForeignKey(Patient)
    medication_name = models.CharField(max_length=1000, blank=False, null=False, verbose_name='Medication Name')
    date_started = models.DateField(blank=False, null=True, verbose_name='Date Started')
    dosage_form = models.CharField(max_length=100, verbose_name='Dosage Form')
    strength = models.CharField(max_length=1000, blank=False, null=False, verbose_name='Strength')

    def __str__(self):
        return 'Medication for %s %s'%(self.patient.first_name, self.patient.last_name)


class Allergy(models.Model):
    """
    Allergies
    """
    patient = models.ForeignKey(Patient)
    allergen_name = models.CharField(max_length=1000, blank=False, null=False, verbose_name='Name of Allergen')
    reaction = models.CharField(max_length=1000, blank=False, null=False, verbose_name='Reaction')
    severity = models.CharField(max_length=1000, blank=False, null=False, verbose_name='Severity')
    allergen_type = models.CharField(max_length=1000, blank=False, null=False, choices=ALLERGEN_TYPE, 
                                    verbose_name='Allergen Type')

    def __str__(self):
            return 'Allergy for %s %s'%(self.patient.first_name, self.patient.last_name)

class Surgery(models.Model):
    """
    Surgeries
    """
    patient = models.ForeignKey(Patient)
    procedure_name = models.CharField(max_length=1000, blank=False, null=False, verbose_name='Name of Procedure')
    date = models.DateField(blank=False, null=False, verbose_name='Date')
    surgeon_name = models.CharField(max_length=1000, blank=False, null=False, verbose_name='Name of Surgeon')

    def __str__(self):
        return 'Surgery for %s %s'%(self.patient.first_name, self.patient.last_name)


class FamilyHistory(models.Model):
    """
    Family history
    """
    patient = models.ForeignKey(Patient)
    disease = models.CharField(max_length=1000, blank=False, null=False, verbose_name='Disease')
    relationship = models.CharField(max_length=1000, blank=False, null=False, verbose_name='Relationship')
    details = models.CharField(max_length=1000, blank=False, null=False, verbose_name='Details')
    status = models.CharField(max_length=100, blank=False, null=False, verbose_name='Status')
    
    def __str__(self):
        return 'Family History for %s %s'%(self.patient.first_name, self.patient.last_name)







