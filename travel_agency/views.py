from django.http import HttpResponse
from django.shortcuts import render
from .models import Destination

# Create your views here.

def index(request):
    return render(request, 'travel_agency/index.html')

def allusers(request):
	return render(request, 'travel_agency/allusers.html', Destination.get_all())