from django.contrib.auth.models import User
from django.db import models, connection
from django.core.validators import MinValueValidator

from datetime import datetime

# Create your models here.
cursor = connection.cursor()

class Address(models.Model):
	address_id = models.IntegerField(primary_key=True)
	line1 = models.CharField(max_length=50)
	line2 = models.CharField(max_length=50)
	city = models.CharField(max_length=35)
	state = models.CharField(max_length=2)
	country = models.CharField(max_length=50)
	zip_code = models.IntegerField()

class Payment(models.Model):
	payment_id = models.IntegerField(primary_key=True)
	credit_no = models.IntegerField()
	expiry = models.DateField(default=datetime.now)

class Profile(models.Model):
	profile_id = models.IntegerField(primary_key=True)
	user_id = models.OneToOneField(User, on_delete="CASCADE")
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	home_addr = models.OneToOneField(Address, on_delete="CASCADE", related_name='profile_home_addr')
	billing_addr = models.OneToOneField(Address, on_delete="CASCADE", related_name='profile_billing_addr')
	payment_method = models.ForeignKey(Payment, on_delete="DO_NOTHING")
	email = models.CharField(max_length=254)

class Location(models.Model):
	location_id = models.IntegerField(primary_key=True)
	city = models.CharField(max_length=35)
	state = models.CharField(null=True, max_length=2)
	country = models.EmailField()

class Travel(models.Model):
	travel_id = models.IntegerField(primary_key=True)
	user_id = models.IntegerField()
	from_location = models.ForeignKey(Location, on_delete="DO_NOTHING", related_name='travel_from_location')
	to_location = models.ForeignKey(Location, on_delete="DO_NOTHING", related_name='travel_to_location')
	payment_id = models.IntegerField()
	travel_date = models.DateField(default=datetime.now)
	
	# def get_all():
	# 	cursor.execute('SELECT COUNT(*) FROM travel_agency_location')
	# 	result = cursor.fetchall()[0][0]

	# 	return { 'result': result }

class Search(models.Model):
	search_id = models.IntegerField(primary_key=True)
	user_id = models.IntegerField()
	from_location = models.ForeignKey(Location, on_delete="DO_NOTHING", related_name='search_from_location')
	to_location = models.ForeignKey(Location, on_delete="DO_NOTHING", related_name='search_to_location')
	from_date = models.DateField(default=datetime.now)
	to_date = models.DateField(default=datetime.now)
	travelers_count = models.IntegerField(validators=[MinValueValidator(1)])

class Transportation(models.Model):
	transport_id = models.IntegerField(primary_key=True)
	number = models.IntegerField()
	carrier = models.CharField(max_length=20)
	location = models.ForeignKey(Location, on_delete="DO_NOTHING")
	cost = models.IntegerField()

class Flight(Transportation):
	CLASS_CHOICES = (
		('ECONOMY', 'economy'),
		('BUSINESS', 'business'),
		('FIRST', 'first')
	)

	flight_id = models.IntegerField(primary_key=True)
	flight_class = models.CharField(max_length=10, choices=CLASS_CHOICES)

class Car(Transportation):
	CLASS_CHOICES = (
		('COMMERCIAL', 'commercial'),
		('CONVERTIBLE', 'convertible'),
		('VAN', 'van'),
		('TRUCK', 'truck'),
		('LUXURY', 'luxury'),
		('SUV', 'suv')
	)

	car_id = models.IntegerField(primary_key=True)
	car_confirmation_id = models.IntegerField()
	car_class = models.CharField(max_length=10, choices=CLASS_CHOICES)

class Cruise(Transportation):
	cruise_id = models.IntegerField(primary_key=True)

connection.close()