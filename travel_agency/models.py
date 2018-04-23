from django.db import models, connection
import datetime

# Create your models here.
cursor = connection.cursor()

class Destination(models.Model):
	
	travel_id = models.IntegerField(primary_key=True)
	user_id = models.IntegerField()
	location_id = models.IntegerField()
	payment_id = models.IntegerField()
	travel_date = models.DateField()
	
	def get_all():
		cursor.execute('SELECT COUNT(*) FROM travel_agency_destination')
		result = cursor.fetchall()[0][0]

		return { 'result': result }

connection.close()