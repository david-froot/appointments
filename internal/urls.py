from django.conf.urls import url
from views import dentist_views, referral_views, admin_views


urlpatterns = [

    # Form views for dentists:
    url(r'^dentist/dashboard/$', dentist_views.dashboard, name='d-dashboard'),

    # Views for reffered dentists:
    url(r'^referral/dashboard/$', referral_views.dashboard, name='r-dashboard'),    
    url(r'^referral/patients/$', referral_views.patients, name='r-patients'),    
    url(r'^referral/patients/(?P<id>[0-9]+)/$', referral_views.patient_history, name='h-patientinfo'),
    url(r'^referral/appointment/(?P<id>[0-9]+)/$', referral_views.appointment_details, name='r-appt'),


	url(r'^staff/dashboard/$', admin_views.dashboard, name='s-dashboard'),    

]







"""
url(r'^patient/view/', views.view_patients),
url(r'^patient/billing/', views.billing_view),

# Appointment management:
url(r'^sitevisit/view/', views.view_site_visits),
url(r'^sitevisit/add/', views.CreateCompanyVisitView.as_view()),    
url(r'^sitevisit/info/(?P<visit_id>[0-9]+)/$', views.info_site_visit),


url(r'^appointment/info/(?P<apt_id>[0-9]+)/$', views.AppointmentInfoFormView.as_view()),
#url(r'^admin/appointment/block/(?P<apt_id>[0-9]+)/$', views.block_appointment_slot),
url(r'^appointment/files/(?P<apt_id>[0-9]+)/$', views.view_files),
url(r'^appointment/info/(?P<apt_id>[0-9]+)/(?P<fname>[0-9A-Za-z_\-]+)', views.view_files),
url(r'^appointment/togglesetting/(?P<apt_id>[0-9]+)/$', views.toggle_setting),
"""