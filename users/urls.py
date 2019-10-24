from django.conf.urls import include, url
from users import views
from django.contrib.auth.views import password_reset


urlpatterns = [
    
    url(r'^login/', views.LoginUser.as_view(), name='login' ),
    url(r'^logout/', views.logoutUser, name='logout' ),
    url(r'^changepassword/', views.ResetPassword.as_view(), name='changepw' ),
    #url(r'^confirmemail/(?P<token>.*)/', views.confirm_email, name='confirmemail' ),
    url(r'^changeemail', views.ChangeEmail.as_view(), name='changeemail' ),
    url(r'^resetpassword/', views.reset_password, name='resetpassword' ),
    url(r'^resetcode/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.reset_confirm, name='resetcode'),
    url(r'^success/', views.success, name='success'),
    url(r'^settings/', views.settings, name='settings'),

]

