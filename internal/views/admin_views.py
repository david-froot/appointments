"""

Views for admins / high level staff 

DLF 2017

"""
from django.shortcuts import render, redirect


def dashboard(request):
	'''
	Home page for staff
	'''
	return render(request, 'internal/admin/dashboard.html')



def toggle_setting(request, apt_id):
	"""
	Toggle different patient boolean fields
	"""
	attr = request.GET.get('attr', None)
	if attr not in ('is_paid', 'reimbursement_confirmed',
				'billing_recieved', 'billing_sent','is_break'):
		return Http404
	
	visit = get_object_or_404(PatientAppointmentSlot, id=apt_id)

	# Invert the attribute:
	setattr(visit, attr, not getattr(visit, attr))
	visit.save()    
	return HttpResponse('Success')