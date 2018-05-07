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
    state = models.CharField(max_length=35)
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

    def __str__(self):
        return self.name

    def get_company(company_id):
        cursor = connection.cursor()
        try:
            query = '''
                SELECT *
                FROM travel_agency_company
                WHERE company_id=%s
            '''
            cursor.execute(query, (company_id,))
            result = cursor.fetchone()
        finally:
            connection.close()

        return result

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
   
    def search(from_location, to_location, date, travelers_count, price, time):
        cursor = connection.cursor()
        try:
            query = '''
                SELECT flight_id, name, from_date, flight_class, city, state, cost, available
                FROM (
                    SELECT *
                    FROM travel_agency_flight
                    INNER JOIN travel_agency_location ON travel_agency_flight.from_location_id=travel_agency_location.location_id
                    INNER JOIN travel_agency_company ON travel_agency_flight.company_id=travel_agency_company.company_id
                )
                WHERE   city=%s AND
                        available >= %s AND
                        from_date LIKE %s 
            '''
            if to_location is not '':
                query += 'AND to_location_id = (SELECT location_id FROM travel_agency_location WHERE city = \''+to_location + '\')'
            if int(price) == 1:
                query += " ORDER BY cost "
            elif int(price) == 2:
                query += " ORDER BY cost DESC "
            if int(time) == 1:
                if "ORDER BY" not in query:
                    query += " ORDER BY to_date-from_date "
                else:
                    query += ", to_date-from_date"
            elif int(time) == 2:
                if "ORDER BY" not in query:
                    query += " ORDER BY to_date-from_date DESC "
                else:
                    query += ", to_date-from_date DESC"
            cursor.execute(query, (from_location, travelers_count, date+'%'))
            results = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
        finally:
            connection.close()

        return results

    def search_one_stop(from_location, to_location, date, travelers_count, price, time):
        cursor = connection.cursor()
        try:
            query = '''
                SELECT  a.flight_id, a.city, a.name, a.cost, a.available, a.flight_class,
                    b.flight_id, b.city, b.name, b.cost, b.available, b.flight_class
                FROM (
                    SELECT *
                    FROM travel_agency_flight
                    INNER JOIN travel_agency_location 
                    ON travel_agency_flight.from_location_id=travel_agency_location.location_id
                    INNER JOIN travel_agency_company 
                    ON travel_agency_flight.company_id=travel_agency_company.company_id
                ) a, (
                    SELECT *
                    FROM travel_agency_flight
                    INNER JOIN travel_agency_location 
                    ON travel_agency_flight.to_location_id=travel_agency_location.location_id
                    INNER JOIN travel_agency_company 
                    ON travel_agency_flight.company_id=travel_agency_company.company_id
                ) b
                WHERE   a.city=%s AND
                        a.to_location_id=b.from_location_id AND
                        b.city=%s AND 
                        a.available >= %s AND
                        b.available >= %s AND 
                        a.from_date LIKE %s AND
                        b.from_date >= a.to_date
            '''
            if int(price) == 1:
                query += " ORDER BY a.cost, b.cost "
            elif int(price) == 2:
                query += " ORDER BY a.cost DESC, b.cost DESC "
            if int(time) == 1:
                if "ORDER BY" not in query:
                    query += " ORDER BY a.to_date-a.from_date, b.to_date-b.from_date "
                else:
                    query += ", a.to_date-a.from_date, b.to_date-b.from_date"
            elif int(time) == 2:
                if "ORDER BY" not in query:
                    query += " ORDER BY a.to_date-a.from_date DESC, b.to_date-b.from_date DESC "
                else:
                    query += ", a.to_date-a.from_date DESC, b.to_date-b.from_date DESC"

            cursor.execute(query, (from_location, to_location, travelers_count, travelers_count, date+'%'))
            descriptions = ('a_flight_id', 'a_city', 'a_name', 'a_cost', 'a_available', 'a_flight_class', 'b_flight_id', 'b_city', 'b_name', 'b_cost', 'b_available', 'b_flight_class')
            results = [dict((descriptions[i], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
        finally:
            connection.close()

        return results

    def get_flight(flight_id):
        cursor = connection.cursor()
        try:
            query = '''
                SELECT * 
                FROM travel_agency_flight
                WHERE travel_agency_flight.flight_id = %s
            '''
            cursor.execute(query, (flight_id,))
            results = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
        finally:
            connection.close()

        return results

    def purchase(flight_id, travelers_count):
        cursor = connection.cursor()
        try:
            query = '''
                UPDATE travel_agency_flight
                SET available=available-%s
                WHERE flight_id=%s
            '''
            cursor.execute(query, (travelers_count, flight_id))
        finally:
            connection.close()

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

    def search(pickup_location, dropoff_location, from_date, to_date, price):
        cursor = connection.cursor()
        try:
            query = '''
            SELECT name, car_id, car_class, confirmation_id, available, cost, from_date, to_date 
            FROM (
                SELECT *
                FROM travel_agency_car
                INNER JOIN travel_agency_location 
                ON travel_agency_car.from_location_id=travel_agency_location.location_id
                INNER JOIN travel_agency_company
                ON travel_agency_car.company_id=travel_agency_company.company_id
            )
            WHERE city=%s 
                AND available >= 1 
                AND from_date LIKE %s 
                AND to_date >= %s
                AND to_location_id = (
                    SELECT location_id 
                    FROM travel_agency_location 
                    WHERE city = %s
                ) 
            '''
            if int(price) == 1:
                query += " ORDER BY cost "
            elif int(price) == 2:
                query += " ORDER BY cost DESC "

            cursor.execute(query, (pickup_location, from_date+'%', to_date, dropoff_location))
            results = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
        finally:
            connection.close()

        return results

    def get_car(car_id):
        cursor = connection.cursor()
        try:
            query = '''
                SELECT * 
                FROM travel_agency_car
                WHERE travel_agency_car.car_id = %s
            '''
            cursor.execute(query, (car_id,))
            results = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
        finally:
            connection.close()

        return results

    def purchase(car_id):
        cursor = connection.cursor()
        try:
            query = '''
                UPDATE travel_agency_car
                SET available=available-1
                WHERE car_id=%s
            '''
            cursor.execute(query, (car_id,))
        finally:
            connection.close()

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

    def search(from_location, to_location, travelers_count, from_date, to_date):
        cursor = connection.cursor()
        try:
            cursor.execute('''
                SELECT name, from_date, to_date, city, country, cost, available, cruise_id
                FROM (
                    SELECT *
                    FROM travel_agency_cruise
                    INNER JOIN travel_agency_location ON travel_agency_cruise.from_location_id=travel_agency_location.location_id
                    INNER JOIN travel_agency_company ON travel_agency_cruise.company_id=travel_agency_company.company_id
                )
                WHERE   city=%s AND
                        available >= %s AND
                        from_date LIKE %s AND
                        to_date LIKE %s
            ''', (from_location, travelers_count, from_date+'%', to_date+'%'))
            results = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
        finally:
            connection.close()

        return results

    def get_cruise(cruise_id):
        cursor = connection.cursor()
        try:
            query = '''
                SELECT * 
                FROM travel_agency_cruise
                WHERE travel_agency_cruise.cruise_id = %s
            '''
            cursor.execute(query, (cruise_id,))
            results = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
        finally:
            connection.close()

        return results

    def purchase(cruise_id):
        cursor = connection.cursor()
        try:
            query = '''
                UPDATE travel_agency_cruise
                SET available=available-1
                WHERE cruise_id=%s
            '''
            cursor.execute(query, (cruise_id,))
        finally:
            connection.close()


class Amenities(models.Model):
    amenities_id = models.IntegerField(primary_key=True)
    breakfast = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    fitness = models.BooleanField(default=False)
    pool = models.BooleanField(default=False)
    bar = models.BooleanField(default=False)
    wifi = models.BooleanField(default=False)

class Hotel(models.Model):
    hotel_id = models.IntegerField(primary_key=True)
    company = models.ForeignKey(Company, on_delete="DO_NOTHING", default=1)
    addr = models.OneToOneField(Address, on_delete="CASCADE")
    cost = models.IntegerField(default=0)
    available = models.IntegerField(default=0)
    from_date = models.DateTimeField(default=datetime.now)
    to_date = models.DateTimeField(default=datetime.now)
    amenities = models.OneToOneField(Amenities, on_delete="CASCADE")

    def search(location, rooms_count, from_date, to_date, breakfast, bar, wifi, gym, pool, parking):
        cursor = connection.cursor()
        try:
            query = '''
                SELECT name, from_date, to_date, city, cost, available, hotel_id, breakfast, parking, fitness, pool, bar, wifi
                FROM (
                    SELECT *
                    FROM travel_agency_hotel
                    INNER JOIN travel_agency_address ON travel_agency_hotel.addr_id=travel_agency_address.address_id
                    INNER JOIN travel_agency_company ON travel_agency_hotel.company_id=travel_agency_company.company_id
                    INNER JOIN travel_agency_amenities ON travel_agency_hotel.amenities_id=travel_agency_amenities.amenities_id
                )
                WHERE   city=%s AND
                        available >= %s AND
                        from_date <= %s AND
                        to_date >= %s
            '''
            if breakfast:
                query += 'AND breakfast = 1'
            if bar:
                query += 'AND bar = 1'
            if pool:
                query += 'AND pool = 1'
            if wifi:
                query += 'AND wifi = 1'
            if parking:
                query += 'AND parking = 1'
            if gym:
                query += 'AND gym = 1'

            cursor.execute(query, (location, rooms_count, from_date, to_date))
            results = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
        finally:
            connection.close()

        return results

    def get_hotel(hotel_id):
        cursor = connection.cursor()
        try:
            query = '''
                SELECT * 
                FROM travel_agency_hotel
                WHERE travel_agency_hotel.hotel_id = %s
            '''
            cursor.execute(query, (hotel_id,))
            results = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
        finally:
            connection.close()

        return results

    def purchase(hotel_id):
        cursor = connection.cursor()
        try:
            query = '''
                UPDATE travel_agency_hotel
                SET available=available-1
                WHERE hotel_id=%s
            '''
            cursor.execute(query, (hotel_id,))
        finally:
            connection.close()

class Review(models.Model):
    review_id = models.IntegerField(primary_key=True)
    company_id = models.ForeignKey(Company, on_delete="DO_NOTHING")
    user_id = models.ForeignKey(User, on_delete="DO_NOTHING")
    content = models.CharField(max_length=256)
    rating = models.IntegerField()
    date = models.DateField(default=datetime.now)

    def get_reviews(company_name):
        cursor = connection.cursor()
        try:
            query = '''
                SELECT *
                FROM travel_agency_review
                INNER JOIN travel_agency_company
                ON travel_agency_review.company_id_id=travel_agency_company.company_id
                WHERE name=%s
            '''
            cursor.execute(query, (company_name,))
            results = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
        finally:
            connection.close()

        return results

class Orders(models.Model):
    TYPE_CHOICES = (
        ('FLIGHT', 'flight'),
        ('CRUISE', 'cruise'),
        ('CAR', 'car'),
        ('HOTEL', 'hotel')
    )
    order_id = models.IntegerField(primary_key=True)
    user_id = models.OneToOneField(User, unique=False, on_delete="DO_NOTHING")
    order_type = models.CharField(max_length=6, choices=TYPE_CHOICES)
    order_type_id = models.IntegerField(unique=False)
    travelers_count = models.IntegerField(unique=False)

    def get_orders(user):
        cursor = connection.cursor()
        try:
            query = '''
                SELECT cost, flight_class, from_date, to_date, name, a.city as from_city, b.city as to_city, travelers_count
                FROM travel_agency_flight
                INNER JOIN travel_agency_orders ON
                travel_agency_flight.flight_id = travel_agency_orders.order_type_id
                INNER JOIN travel_agency_company ON 
                travel_agency_flight.company_id=travel_agency_company.company_id
                INNER JOIN travel_agency_location a ON
                travel_agency_flight.from_location_id=a.location_id
                INNER JOIN travel_agency_location b ON
                travel_agency_flight.to_location_id=b.location_id
                WHERE user_id_id = 
                (SELECT id FROM auth_user WHERE username=%s)
                AND order_type='flight'
            '''
            cursor.execute(query, (str(user),))
            results = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]

            query = '''
                SELECT cost, car_class, from_date, to_date, name, a.city as from_city, b.city as to_city, available
                FROM travel_agency_car
                INNER JOIN travel_agency_orders ON
                travel_agency_car.car_id = travel_agency_orders.order_type_id
                INNER JOIN travel_agency_company ON 
                travel_agency_car.company_id=travel_agency_company.company_id
                INNER JOIN travel_agency_location a ON
                travel_agency_car.from_location_id=a.location_id
                INNER JOIN travel_agency_location b ON
                travel_agency_car.to_location_id=b.location_id
                WHERE user_id_id = 
                (SELECT id FROM auth_user WHERE username=%s)
                AND order_type = 'car'
            '''
            cursor.execute(query, (str(user),))
            results += [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]

            query = '''
                SELECT *
                FROM travel_agency_hotel
                INNER JOIN travel_agency_orders ON
                travel_agency_hotel.hotel_id = travel_agency_orders.order_type_id
                INNER JOIN travel_agency_company ON 
                travel_agency_hotel.company_id=travel_agency_company.company_id
                INNER JOIN travel_agency_address ON
                travel_agency_hotel.addr_id=travel_agency_address.address_id
                WHERE user_id_id = 
                (SELECT id FROM auth_user WHERE username=%s)
                AND order_type = 'hotel'
            '''
            cursor.execute(query, (str(user),))
            results += [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]

            query = '''
                SELECT cost, from_date, to_date, name, a.city as from_city, b.city as to_city, travelers_count
                FROM travel_agency_cruise
                INNER JOIN travel_agency_orders ON
                travel_agency_cruise.cruise_id = travel_agency_orders.order_type_id
                INNER JOIN travel_agency_company ON 
                travel_agency_cruise.company_id=travel_agency_company.company_id
                INNER JOIN travel_agency_location a ON
                travel_agency_cruise.from_location_id=a.location_id
                INNER JOIN travel_agency_location b ON
                travel_agency_cruise.to_location_id=b.location_id
                WHERE user_id_id = 
                (SELECT id FROM auth_user WHERE username=%s)
                AND order_type = 'cruise'
            '''
            cursor.execute(query, (str(user),))
            results += [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
        finally:
            connection.close()

        return results

    def add_order(user, order_type, order_type_id, travelers_count):
        cursor = connection.cursor()
        try:
            query = '''
                INSERT INTO travel_agency_orders (order_type, order_type_id, travelers_count, user_id_id)
                VALUES (%s, %s, %s, (SELECT id FROM auth_user WHERE username=%s))
            '''
            cursor.execute(query, (str(order_type), int(order_type_id), int(travelers_count), str(user),))
        finally:
            connection.close()