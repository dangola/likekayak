from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login_user, name='login'),
    url(r'^logout/', views.logout_user, name='logout'),
    url(r'^flights/', views.flights, name='flights'),
    url(r'^cars/', views.cars, name='cars'),
    url(r'^packages/', views.packages, name='packages'),
    url(r'^settings/', views.settings, name='settings'),
    url(r'^hotels/', views.hotels, name='hotels'),
]