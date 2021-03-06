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
            non_stop = request.POST.get('non_stop', False) == 'on'
            one_stop = request.POST.get('one_stop', False) == 'on'

            if not non_stop and not one_stop:
                non_stop = True

            if non_stop:
                context['non_stop_departure_flights'] = Flight.search(from_location, to_location, from_date, travelers_count, price, time)
            if one_stop:
                context['one_stop_departure_flights'] = Flight.search_one_stop(from_location, to_location, from_date, travelers_count, price, time)
            context['to_location'] = to_location
            context['travelers_count'] = travelers_count
            if round_trip:
                if non_stop:
                    context['non_stop_return_flights'] = Flight.search(to_location, from_location, to_date, travelers_count, price, time)
                if one_stop:
                    context['one_stop_return_flights'] = Flight.search_one_stop(to_location, from_location, to_date, travelers_count, price, time)
                context['return_to_location'] = from_location
            print(non_stop, one_stop)
            print(context)
            if 'non_stop_departure_flights' in context or 'one_stop_departure_flights' in context:
                if round_trip and (non_stop and context['non_stop_return_flights'] == []) and (one_stop and context['one_stop_return_flights'] == []):
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
    form = CarSearchForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            from_date = request.POST['from_date']
            to_date = request.POST['to_date']
            pickup_location = request.POST['pickup_location']
            dropoff_location = request.POST['dropoff_location']
            price = request.POST.get('price')
            same_pickup = request.POST.get('same_pickup', False) == 'on'

            context = { 
                'cars': Car.search(pickup_location, dropoff_location, from_date, to_date, price, same_pickup),
                'pickup_location': pickup_location,
                'dropoff_location': dropoff_location
            }

            return render(request, 'travel_agency/cars.html', context)
        return render(request, 'travel_agency/cars.html', {'error_message': form.errors.as_text})
    context = {
        'form': form,
    }
    return render(request, 'travel_agency/cars.html', context)

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

def hotels(request):
    form = HotelsForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            location = request.POST['location']
            rooms_count = request.POST['rooms_count']
            from_date = request.POST['from_date']
            to_date = request.POST['to_date']
            breakfast = request.POST.get('breakfast', False) == 'on'
            bar = request.POST.get('bar', False) == 'on'
            wifi = request.POST.get('wifi', False) == 'on'
            gym = request.POST.get('gym', False) == 'on'
            pool = request.POST.get('pool', False) == 'on'
            parking = request.POST.get('parking', False) == 'on'

            context = {
                'available_hotels': Hotel.search(location, rooms_count, from_date, to_date, breakfast, bar, wifi, gym, pool, parking),
                'location': location,
                'rooms_count': rooms_count
            }
            if context['available_hotels']:
                return render(request, 'travel_agency/hotels.html', context)
            else:
                return render(request, 'travel_agency/hotels.html', {'error_message': 'Oops! We don\'t have any rooms available for that.'})
        else:
            return render(request, 'travel_agency/hotels.html', {'error_message': form.errors.as_text})
    
    context = {
        'form': form,
    }
    return render(request, 'travel_agency/hotels.html', context)

def select(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        context = {}
        if 'flight_id' in data:
            flight = Flight.get_flight(data['flight_id'])
            context = {'flight_id': flight[0]['flight_id']}
        elif 'car_id' in data:
            car = Car.get_car(data['car_id'])
            context = {'car_id': flight[0]['car_id']}
        elif 'hotel_id' in data:
            hotel = Hotel.get_hotel(data['hotel_id'])
            context = {'hotel_id': hotel[0]['hotel_id']}
        elif 'cruise_id' in data:
            cruise = Cruise.get_cruise(data['cruise_id'])
            context = {'cruise_id': cruise[0]['cruise_id']}
        return HttpResponse(json.dumps(context), content_type='application/json')

def purchase(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        context = { }
        if 'flight_id' in data and data['flight_id'] is not None:
            Flight.purchase(data['flight_id'], data['travelers_count'])
            if request.user.is_authenticated:
                Orders.add_order(request.user, 'flight', data['flight_id'], data['travelers_count'])
            flight = Flight.get_flight(data['flight_id'])
            context = {'available': flight[0]['available']}
        elif 'car_id' in data and data['car_id'] is not None:
            Car.purchase(data['car_id'])
            if request.user.is_authenticated:
                Orders.add_order(request.user, 'car', data['car_id'], 1)
            car = Car.get_car(data['car_id'])
            context = {'available': car[0]['available']}
        elif 'hotel_id' in data and data['hotel_id'] is not None:
            Hotel.purchase(data['hotel_id'])
            if request.user.is_authenticated:
                Orders.add_order(request.user, 'hotel', data['hotel_id'], 1)
            hotel = Hotel.get_hotel(data['hotel_id'])
            context = {'available': hotel[0]['available']}
        elif 'cruise_id' in data and data['cruise_id'] is not None:
            Cruise.purchase(data['cruise_id'])
            if request.user.is_authenticated:
                Orders.add_order(request.user, 'cruise', data['cruise_id'], 1)
            cruise = Cruise.get_cruise(data['cruise_id'])
            context = {'available': cruise[0]['available']}
        return HttpResponse(json.dumps(context), content_type='application/json')

def orders(request):
    context = {
        'orders': Orders.get_orders(request.user)
    }
    return render(request, 'travel_agency/orders.html', context)

def review(request):
    form = ReviewForm(request.POST or None)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return render(request, 'travel_agency/review.html', {'error_message': 'You need to be logged in to post a review.'})

        content = request.POST['content']
        rating = form.save(commit=False)
        rating.user_id = request.user
        rating.rating = request.POST['rating']
        rating.company_id = Company.objects.get(company_id=request.POST['company'])
        rating.save()
        return render(request, 'travel_agency/review.html', {})
    context = {
        'form': form
    }
    return render(request, 'travel_agency/review.html', context)

def review_company(request, company_name):
    context = {
        'reviews': Review.get_reviews(company_name)
    }
    if context['reviews']:
        return render(request, 'travel_agency/reviews.html', context)
    else:
        return render(request, 'travel_agency/reviews.html', {'error_message': 'Sorry! This company has no reviews!'})

def cruises(request):
    form = CruiseSearchForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            from_location = request.POST['from_location']
            to_location = request.POST['to_location']
            travelers_count = request.POST['travelers_count']
            from_date = request.POST['from_date']
            to_date = request.POST['to_date']
            context = {
                'available_cruises': Cruise.search(from_location, to_location, travelers_count, from_date, to_date),
                'from_location': from_location,
                'to_location': to_location,
                'travelers_count': travelers_count
            }
            if context['available_cruises']:
                return render(request, 'travel_agency/cruises.html', context)
            else:
                return render(request, 'travel_agency/cruises.html', {'error_message': 'Oops! We don\'t have any rooms available for that.'})
        else:
            return render(request, 'travel_agency/cruises.html', {'error_message': form.errors.as_text})
    
    context = {
        'form': form,
    }
    return render(request, 'travel_agency/cruises.html', context)
