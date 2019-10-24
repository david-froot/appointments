"""

Base views for all users regardless of type 

DLF 2017

"""
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.shortcuts import render, redirect
from forms import LoginForm, ChangeEmailForm, PasswordResetForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import  FormView
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse


class LoginUser(FormView):

    form_class = LoginForm
    template_name = 'users/login.html'
    success_url = '/'

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password']) 
        if user is not None and user.is_active:
            login(self.request, user)
            print user.get_dashboard()
            return redirect(user.get_dashboard())
        return super(LoginUser, self).form_valid(form)


class ResetPassword(FormView):

    form_class = PasswordResetForm
    template_name = 'users/form.html'
    success_url = '/users/success/'

    def form_valid(self, form):
        self.request.user.set_password(form.cleaned_data['password'])
        self.request.user.save()
        return super(ResetPassword, self).form_valid(form)
        

class ChangeEmail(FormView):

    form_class = ChangeEmailForm
    template_name = 'users/form.html'
    success_url = '/users/success/'

    def form_valid(self, form):
        #send_confirm_email(request.user,form.cleaned_data['email'])
        self.request.user.email = form.cleaned_data['email']
        self.request.user.save()
        return super(ChangeEmail, self).form_valid(form)


def settings(request):
    return render(request, 'users/settings.html', 
            { 'passwordform' : PasswordResetForm(),
              'emailform'    : ChangeEmailForm() })


def logoutUser(request):
    logout(request)
    return redirect('/')


def reset_password(request):
    return password_reset(request, template_name='users/form.html',
                        email_template_name='users/reset_email.html',
                        post_reset_redirect='/users/success/')


def reset_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request, 
        template_name='users/form.html',
        uidb64=uidb64, token=token, 
        post_reset_redirect='/users/login/')


def success(request):
    return render(request, "users/resetsuccess.html")
