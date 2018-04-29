from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View
from .forms import UserForm, SearchForm

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
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'travel_agency/login.html', context)

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