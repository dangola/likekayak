# likekayak
A mimic, minimal version of travel agency site Kayak

To host the server on localhost run the following:

```
python manage.py runserver
```

To make commit model changes and synchronize the database run the following:
```
python manage.py makemigrations travel_agency
python manage.py migrate
```

To import data into the database, place json files in `travel_agency/fixtures/` and run the following:
```
python manage.py loaddata travel_agency/fixtures/<file_path>
```
