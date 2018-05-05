from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View
from .forms import *
from .models import *
import json
# Create your views here.

def index(request):
    return render(request, 'travel_agency/index.html')

def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'travel_agency/index.html')
    context = {
        'form': form,
    }
    return render(request, 'travel_agency/register.html', context)

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'travel_agency/index.html')
            else:
                return render(request, 'travel_agency/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'travel_agency/login.html', {'error_message': 'Invalid login'})
    return render(request, 'travel_agency/login.html')

def logout_user(request):
    logout(request)
    form = UserForm()
    context = {
        "form": form,
    }
    return render(request, 'travel_agency/login.html', context)

def flights(request):
    form = SearchForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid(): 
            context = {}
            from_location = request.POST['from_location']
            to_location = request.POST['to_location']
            from_date = request.POST['from_date']
            to_date = request.POST['to_date']
            travelers_count = request.POST['travelers_count']
            round_trip = request.POST.get('round_trip', False)
            price = request.POST.get('price')
            time = request.POST.get('time')
            review = request.POST.get('sort')
            non_stop = request.POST.get('non_stop', False)
            one_stop = request.POST.get('one_stop', False)
            two_stop = request.POST.get('two_stop', False)

            context['departure_flights'] = Flight.search(from_location, to_location, from_date, travelers_count, price, time, review)
            context['to_location'] = to_location
            context['travelers_count'] = travelers_count

            if round_trip:
                context['return_flights'] = Flight.search(to_location, from_location, to_date, travelers_count, price, time, review)
                context['return_to_location'] = from_location
            if context['departure_flights']:
                if round_trip and not context['return_flights']:
                    return render(request, 'travel_agency/flights.html', {'error_message': 'Oops! We don\'t have any flights for that.'})  
                else:
                    return render(request, 'travel_agency/flights.html', context)
            else:
                return render(request, 'travel_agency/flights.html', {'error_message': 'Oops! We don\'t have any flights for that.'})
        else:
            return render(request, 'travel_agency/flights.html', {'error_message': form.errors.as_text})
    
    context = {
        'form': form,
    }
    return render(request, 'travel_agency/flights.html', context)

def cars(request):
    return HttpResponse('temp')

def settings(request):
    form = SettingsForm()
    context = {
        'form': form,
    }
    return render(request, 'travel_agency/settings.html', context)

def packages(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            return HttpResponse('good')
        else:
            return render(request, 'travel_agency/packages.html', {'error_message': 'Invalid search'})
    form = SearchForm()
    context = {
        'form': form,
    }
    return render(request, 'travel_agency/packages.html', context)

def select(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        flight = Flight.get_flight(data['flight_id'])
        return HttpResponse(json.dumps({'flight_id': flight[0]['flight_id']}), content_type='application/json')

def purchase(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Flight.purchase(data['flight_id'], data['travelers_count'])
        if request.user.is_authenticated:
            FlightOrders.add_order(request.user, data['flight_id'], data['travelers_count'])
        flight = Flight.get_flight(data['flight_id'])
        return HttpResponse(json.dumps({'available': flight[0]['available']}), content_type='application/json')

def orders(request):
    context = {
        'orders': FlightOrders.get_orders(request.user)
    }
    return render(request, 'travel_agency/orders.html', context)
