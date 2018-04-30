from django.contrib.auth.models import User
from django.db import models, connection
from django.core.validators import MinValueValidator

from datetime import datetime

# Create your models here.

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
    home_addr = models.OneToOneField(Address, on_delete="CASCADE", related_name='profile_home_addr', blank=True, null=True)
    billing_addr = models.OneToOneField(Address, on_delete="CASCADE", related_name='profile_billing_addr', blank=True, null=True)
    payment_method = models.ForeignKey(Payment, on_delete="DO_NOTHING", null=True)
    email = models.CharField(max_length=254)

class Location(models.Model):
    location_id = models.IntegerField(primary_key=True)
    city = models.CharField(max_length=35)
    state = models.CharField(null=True, max_length=2)
    country = models.EmailField()

    def __str__(self):
        return self.city

class Travel(models.Model):
    travel_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    from_location = models.ForeignKey(Location, on_delete="DO_NOTHING", related_name='travel_from_location')
    to_location = models.ForeignKey(Location, on_delete="DO_NOTHING", related_name='travel_to_location')
    payment_id = models.IntegerField()
    travel_date = models.DateField(default=datetime.now)
    
class Search(models.Model):
    search_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    from_location = models.ForeignKey(Location, on_delete="DO_NOTHING", related_name='search_from_location')
    to_location = models.ForeignKey(Location, on_delete="DO_NOTHING", related_name='search_to_location', null=True)
    from_date = models.DateField(default=datetime.now)
    to_date = models.DateField(default=datetime.now, null=True)
    travelers_count = models.IntegerField(validators=[MinValueValidator(1)])

class Company(models.Model):
    company_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)

class Flight(models.Model):
    CLASS_CHOICES = (
        ('ECONOMY', 'economy'),
        ('BUSINESS', 'business'),
        ('FIRST', 'first')
    )

    number = models.CharField(max_length=5, default=00000)
    company = models.ForeignKey(Company, on_delete="DO_NOTHING", default=1)
    from_location = models.ForeignKey(Location, on_delete="DO_NOTHING", default=1, related_name='flight_from_location')
    to_location = models.ForeignKey(Location, on_delete="DO_NOTHING", default=1, related_name='flight_to_location')
    cost = models.IntegerField(default=0)
    available = models.IntegerField(default=0)
    from_date = models.DateTimeField(default=datetime.now)
    to_date = models.DateTimeField(default=datetime.now)
    flight_id = models.IntegerField(primary_key=True)
    flight_class = models.CharField(max_length=10, choices=CLASS_CHOICES)
   
    def search(from_location, to_location, from_date, to_date, travelers_count):
        cursor = connection.cursor()
        try:
            cursor.execute('''
                SELECT name, from_date, flight_class, city, state, cost
                FROM (
                    SELECT *
                    FROM travel_agency_flight
                    INNER JOIN travel_agency_location ON travel_agency_flight.from_location_id=travel_agency_location.location_id
                    INNER JOIN travel_agency_company ON travel_agency_flight.company_id=travel_agency_company.company_id
                )
                WHERE   city=%s AND
                        available >= %s AND
                        from_date LIKE %s
            ''', (from_location, travelers_count, from_date+'%'))
            result = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
        finally:
            connection.close()

        return result

class Car(models.Model):
    CLASS_CHOICES = (
        ('COMMERCIAL', 'commercial'),
        ('CONVERTIBLE', 'convertible'),
        ('VAN', 'van'),
        ('TRUCK', 'truck'),
        ('LUXURY', 'luxury'),
        ('SUV', 'suv')
    )

    number = models.CharField(max_length=5, default=00000)
    company = models.ForeignKey(Company, on_delete="DO_NOTHING", default=1)
    from_location = models.ForeignKey(Location, on_delete="DO_NOTHING", default=1, related_name='car_from_location')
    to_location = models.ForeignKey(Location, on_delete="DO_NOTHING", default=1, related_name='car_to_location')
    cost = models.IntegerField(default=0)
    available = models.IntegerField(default=0)
    from_date = models.DateTimeField(default=datetime.now)
    to_date = models.DateTimeField(default=datetime.now)
    car_id = models.IntegerField(primary_key=True)
    confirmation_id = models.IntegerField()
    car_class = models.CharField(max_length=10, choices=CLASS_CHOICES)

    def search(from_location, to_location, from_date, to_date, travelers_count):
        cursor = connection.cursor()
        try:
            cursor.execute('''
                SELECT name, from_date, flight_class, city, state, cost
                FROM (
                    SELECT *
                    FROM travel_agency_flight
                    INNER JOIN travel_agency_location ON travel_agency_flight.from_location_id=travel_agency_location.location_id
                    INNER JOIN travel_agency_company ON travel_agency_flight.company_id=travel_agency_company.company_id
                )
                WHERE   city=%s AND
                        available >= %s AND
                        from_date LIKE %s
            ''', (from_location, travelers_count, from_date+'%'))
            result = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
        finally:
            connection.close()

        return result

class Cruise(models.Model):
    number = models.CharField(max_length=5, default=00000)
    company = models.ForeignKey(Company, on_delete="DO_NOTHING", default=1)
    from_location = models.ForeignKey(Location, on_delete="DO_NOTHING", default=1, related_name='cruise_from_location')
    to_location = models.ForeignKey(Location, on_delete="DO_NOTHING", default=1, related_name='cruise_to_location')
    cost = models.IntegerField(default=0)
    available = models.IntegerField(default=0)
    from_date = models.DateTimeField(default=datetime.now)
    to_date = models.DateTimeField(default=datetime.now)
    cruise_id = models.IntegerField(primary_key=True)

class Amenities(models.Model):
    amenities_id = models.IntegerField(primary_key=True)
    breakfast = models.BooleanField(default=False)
    internet = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    fitness = models.BooleanField(default=False)
    pool = models.BooleanField(default=False)
    bar = models.BooleanField(default=False)

class Hotel(models.Model):
    number = models.CharField(max_length=5, default=00000)
    company = models.ForeignKey(Company, on_delete="DO_NOTHING", default=1)
    location = models.ForeignKey(Location, on_delete="DO_NOTHING", default=1)
    cost = models.IntegerField(default=0)
    available = models.IntegerField(default=0)
    from_date = models.DateTimeField(default=datetime.now)
    to_date = models.DateTimeField(default=datetime.now)
    hotel_id = models.IntegerField(primary_key=True)
    location = models.OneToOneField(Location, on_delete="DO_NOTHING")
    addr = models.OneToOneField(Address, on_delete="CASCADE")
    amenities = models.OneToOneField(Amenities, on_delete="CASCADE")
    cost = models.IntegerField()

class Review(models.Model):
    review_id = models.IntegerField(primary_key=True)
    company_id = models.ForeignKey(Company, on_delete="DO_NOTHING")
    user_id = models.ForeignKey(User, on_delete="DO_NOTHING")
    content = models.CharField(max_length=256)
    rating = models.IntegerField()
    date = models.DateField(default=datetime.now)
