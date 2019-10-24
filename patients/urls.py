from django.conf.urls import url
import views


urlpatterns = [

    # Form views:
    url(r'^forms/$', views.form_overview, name='forms'),
    url(r'^forms/patientinfo/$', views.PatientInformationView.as_view(), name='info'),
    url(r'^forms/healthhistory/$', views.HealthHistoryFormView.as_view(), name='healthhistory'),
    url(r'^forms/medicine/$', views.MedicineFormView.as_view(), name='medicine'),
    url(r'^forms/medicine/delete/(?P<pk>[0-9]+)/$', views.MedicineDeleteView.as_view(), name='medicine-delete'),
    url(r'^forms/surgery/$', views.SurgeryFormView.as_view(), name='surgery'),
    url(r'^forms/surgery/delete/(?P<pk>[0-9]+)/$', views.SurgeryDeleteView.as_view(), name='surgery-delete'),
    url(r'^forms/allergy/$', views.AllergyFormView.as_view(), name='allergy'),
    url(r'^forms/allergy/delete/(?P<pk>[0-9]+)/$', views.AllergyDeleteView.as_view(), name='surgery-delete'),
    url(r'^forms/familyhistory/$', views.FamilyHistoryFormView.as_view(), name='familyhistory'),
    url(r'^forms/familyhistory/delete/(?P<pk>[0-9]+)/$', views.FamilyHistoryDeleteView.as_view(), name='famhist-delete'),
    
    
    # Other views:
    url(r'^register/', views.RegisterPatient.as_view(),name='register' ),
    url(r'^dashboard/', views.dashboard, name='dashboard'),
    url(r'^myhealth/', views.myhealth, name='myhealth'),
    url(r'^settings/', views.settings, name='settings'),
    url(r'^payment/', views.update_payment, name='payment'),


]
