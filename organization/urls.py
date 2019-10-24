from django.conf.urls import url
import views

urlpatterns = [


    url(r'^register/', views.Register.as_view(), name='register'),
    url(r'^dashboard/', views.dashboard, name='dashboard'),
    
    # Vist requests:
    url(r'^visitrequests/$', views.visitrequest_list, name='visitrequest'),
    url(r'^locations/$', views.my_locations, name='locations'),
    url(r'^locations/create/$', views.CreateLocationView.as_view(), name='locations-create'),

    url(r'^visitrequests/create/', views.CreateVisitRequest.as_view(), name='visitrequest-create'),
    url(r'^visitrequests/delete/(?P<pk>[0-9]+)/$', views.VisitRequestDelete.as_view(), name='visitrequest-delete'),
    url(r'^visits/completed/$',views.completed_visits, name="visitrequest-complete"),
    url(r'^visits/completed/rate/(?P<pk>[0-9]+)/$',views.RateVisitView.as_view(), name="visitrequest-rate"),

    

    # Confirmed visits:


    #url(r'^visitdetails/', views.sitevisitrequest_list, name='sitevisits'),

    
]