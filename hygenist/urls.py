from django.conf.urls import url
import views


urlpatterns = [

    # Form views hygenist portal:
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^sitevisit/$', views.my_sitevisits, name='visits'),
    url(r'^sitevisit/(?P<pk>[0-9]+)/$', views.sitevisit_details, name='visitinfo'),
    url(r'^appointment/(?P<pk>[0-9]+)/$', views.AppointmentInfoHygenistFormView.as_view(), name='appt'),
    url(r'^patients/$', views.patient_list, name='patients'),
    url(r'^patients/(?P<patient_id>[0-9]+)/$', views.patient_history, name='patientinfo'),
    url(r'^settings/profilephoto/', views.ProfilePhotoView.as_view(), name='profilephoto'),   
    url(r'^settings/$', views.SettingsView.as_view(), name='settings'),   


]