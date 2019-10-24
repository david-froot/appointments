"""

Views for company HR representitives to manage their account


DLF 2017

"""

from django.views.generic.edit import UpdateView, CreateView, DeleteView, FormView
from django.utils.decorators import method_decorator
from virtudent.virtlib import group_required
from users.models import User, Organization
from datetime import datetime
from models import VisitRequest
from appointments.models import SiteVisit, Location
from django.shortcuts import render
from forms import RegisterForm


@group_required('organization')
def dashboard(request):
    """
    Main dashboard for company representitives
    """
    upcoming = SiteVisit.objects.filter(date__gte=datetime.today().date()).order_by('date')
    return render(request,'organization/dashboard.html',{'upcoming':upcoming})


@group_required('organization')
def my_locations(request):
    """
    Locations for a given organization
    """
    locs = Location.objects.filter(organization=request.user.organization)
    return render(request, 'organization/locations_list.html', {'locations' : locs})



@method_decorator(group_required('organization'), name='dispatch')
class CreateLocationView(CreateView):

    model = Location
    fields = ['name','address','city', 'state', 'zipcode']
    template_name = 'organization/location_form.html'
    success_url = '/organization/locations/'

    def form_valid(self, form):
        form.instance.organization = self.request.user.organization
        return super(CreateLocationView, self).form_valid(form)


@group_required('organization')
def completed_visits(request):
    """
    Previously completed visits
    """

    complete = SiteVisit.objects.filter(date__lt=datetime.today().date()).order_by('-date')
    return render(request, 'organization/completedvisits_list.html', { 'complete': complete })


@group_required('organization')
def visitrequest_list(request):
    """
    Return list of site visit requests
    """
    v = VisitRequest.objects.filter(location__organization=request.user.organization)
    print v
    return render(request, 'organization/visitrequest_list.html', {'visits' : v})



@method_decorator(group_required('organization'), name='dispatch')
class RateVisitView(UpdateView):

    model = SiteVisit
    fields = ['feedback', 'rating']
    template_name='organization/register.html'
    success_url = '/organization/visits/completed/'

    def get_object(self, *args):
        return SiteVisit.objects.get(id=self.kwargs['pk'])



class Register(FormView):
    """
    Register a new company representitve
    """
    form_class = RegisterForm
    template_name = 'organization/register.html'
    success_url = '/'

    def form_valid(self, form):
        user = User.objects.create_user(form.cleaned_data['email'],
                                        form.cleaned_data['email'],
                                        form.cleaned_data['password'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],
                                        phone_number=form.cleaned_data['phone_number'])
        Organization.objects.create(user=user)
        group, created = Group.objects.get_or_create(name='organization')
        group.user_set.add(user)

        return super(Register, self).form_valid(form)


@method_decorator(group_required('organization'), name='dispatch')
class CreateVisitRequest(CreateView):
    '''
    Create a new location for the company
    '''
    model = VisitRequest
    fields = [ 'window_start', 'window_end', 'start', 'end', 'location', 'details']
    template_name='organization/visitrequest_create.html'
    success_url = '/organization/visitrequests/'

    def get_form(self):
        form = super(CreateVisitRequest, self).get_form()
        form.fields['location'].queryset = Location.objects.filter(organization=self.request.user.organization)
        return form

    def form_valid(self, form):
        form.instance.organization = self.request.user.organization
        form.instance.status = 'Pending'
        return super(CreateVisitRequest, self).form_valid(form)


@method_decorator(group_required('organization'), name='dispatch')
class VisitRequestDelete(DeleteView):
    '''
    Delete site visit
    '''   
    model = VisitRequest
    success_url = '/organization/visitrequests/'












'''
from django.conf.urls import *
from django.views.generic import UpdateView
from yourapp.models import Portfolios
from yourapp.forms import PortfoliosCreateForm

urlpatterns = patterns('',
    url('^portfolios/update/(?P<pk>[\w-]+)$', UpdateView.as_view(
        model=Portfolios,
        form_class=PortfoliosCreateForm,
        template_name='portfolios/create.html',
        success_url='/portfolios'
    ), name='portfolio_update'),
)


def get_object(self, queryset=None):
    obj = Portfolios.objects.get(id=self.kwargs['id'])
    return obj


    #def get_object(self, queryset=None):
    #    """ Hook to ensure object is owned by request.user. """
    #   obj = super(MyDeleteView, self).get_object()
    #    if not obj.owner == self.request.user:
    #        raise Http404
    #    return obj
'''
