from django.conf.urls import url
import views


urlpatterns = [

    # Patient-only views
    url(r'^$', views.my_appointments, name='myappts'),
    url(r'^myvisits/', views.view_my_sitevisits, name='visits'),
    url(r'^confirm/(?P<slot_id>[0-9]+)/$', views.confirm_appointment, name='confirm'),
    url(r'^cancel/(?P<slot_id>[0-9]+)/$', views.cancel_appointment, name='cancel'),
    url(r'^pay/(?P<slot_id>[0-9]+)/$', views.confirm_pay_appointment, name='pay'),
    
]