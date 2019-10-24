from django.shortcuts import render, get_object_or_404, redirect


def home(request):
	"""
	Home static view
	"""
	return render(request, 'home.html')


def about(request):
	"""
	About static view
	"""
	return render(request, 'about.html')

def docs(request):
	"""
	API Documentation static view
	"""
	return render(request, 'index.html')