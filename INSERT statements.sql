INSERT INTO Address(pk,line1,line2,city,state,country,zip_code) VALUES (1,'2660 Canyon Boulevard',NULL,'boulder','colorado','united states of america',80302);
INSERT INTO Address(pk,line1,line2,city,state,country,zip_code) VALUES (2,'5397 S Boulder Rd','Hwy 36 & Boulder Rd/ Table Mesa Exit','boulder','colorado','united states of america',80303);

INSERT INTO Amenities(pk,breakfast,parking,fitness,pool,bar,wifi) VALUES (1,'False','True','True','True','True','False');
INSERT INTO Amenities(pk,breakfast,parking,fitness,pool,bar,wifi) VALUES (2,'True','True','False','True','False','True');

INSERT INTO Car(pk,number,company,from_location,to_location,cost,available,from_date,to_date,confirmation_id,car_class) VALUES (0,10001,5,1,3,20,3,'2018-05-20','2018-05-25',18843,'COMMERCIAL');
INSERT INTO Car(pk,number,company,from_location,to_location,cost,available,from_date,to_date,confirmation_id,car_class) VALUES (1,10001,5,1,3,45,3,'2018-05-20','2018-05-27',18842,'TRUCK');
INSERT INTO Car(pk,number,company,from_location,to_location,cost,available,from_date,to_date,confirmation_id,car_class) VALUES (2,10032,6,1,3,20,3,'2018-05-12','2018-05-19',18443,'LUXURY');

INSERT INTO Car(pk,name) VALUES (1,'american airlines');
INSERT INTO Car(pk,name) VALUES (2,'delta airlines');
INSERT INTO Car(pk,name) VALUES (3,'frontier airlines');
INSERT INTO Car(pk,name) VALUES (4,'hertz');
INSERT INTO Car(pk,name) VALUES (5,'avis');
INSERT INTO Car(pk,name) VALUES (6,'alamo');
INSERT INTO Car(pk,name) VALUES (7,'boulder marriott');
INSERT INTO Car(pk,name) VALUES (8,'days hotel by wyndham boulder, boulder');
INSERT INTO Car(pk,name) VALUES (9,'carnival');
INSERT INTO Car(pk,name) VALUES (10,'norwegian cruise line');

INSERT INTO Cruise(pk,number,company,from_location,to_location,cost,available,from_date,to_date) VALUES (0,12345,9,1,8,692,75,'2018-05-20 17:30','2018-05-29 08:48');
INSERT INTO Cruise(pk,number,company,from_location,to_location,cost,available,from_date,to_date) VALUES (1,67890,10,1,9,749,100,'2018-05-20 17:30','2018-05-29 08:48');

INSERT INTO Flight(pk,number,company,from_location,to_location,cost,available,from_date,to_date,flight_class) VALUES (0,34010,1,1,3,1102,73,'2018-05-20 17:30','2018-05-20 08:48','FIRST');
INSERT INTO Flight(pk,number,company,from_location,to_location,cost,available,from_date,to_date,flight_class) VALUES (1,34010,1,3,1,1405,71,'2018-05-20 13:56','2018-05-20 22:26','FIRST');
INSERT INTO Flight(pk,number,company,from_location,to_location,cost,available,from_date,to_date,flight_class) VALUES (7,34010,1,1,3,480,73,'2018-05-20 17:30','2018-05-20 08:48','ECONOMY');
INSERT INTO Flight(pk,number,company,from_location,to_location,cost,available,from_date,to_date,flight_class) VALUES (8,34010,1,3,1,510,71,'2018-05-30 13:56','2018-05-30 22:26','ECONOMY');
INSERT INTO Flight(pk,number,company,from_location,to_location,cost,available,from_date,to_date,flight_class) VALUES (9,34011,2,1,2,500,22,'2018-05-20 13:58','2018-05-20 22:26','ECONOMY');
INSERT INTO Flight(pk,number,company,from_location,to_location,cost,available,from_date,to_date,flight_class) VALUES (2,13136,2,2,3,466,83,'2018-05-23 08:30','2018-05-23 11:54','ECONOMY');
INSERT INTO Flight(pk,number,company,from_location,to_location,cost,available,from_date,to_date,flight_class) VALUES (3,13136,2,3,2,400,42,'2018-06-03 15:20','2018-06-03 16:49','ECONOMY');
INSERT INTO Flight(pk,number,company,from_location,to_location,cost,available,from_date,to_date,flight_class) VALUES (4,62977,2,4,3,919,105,'2018-05-21 22:36','2018-05-21 00:47','ECONOMY');
INSERT INTO Flight(pk,number,company,from_location,to_location,cost,available,from_date,to_date,flight_class) VALUES (5,35513,2,3,6,213,23,'2018-05-25 12:50','2018-05-25 06:22','ECONOMY');
INSERT INTO Flight(pk,number,company,from_location,to_location,cost,available,from_date,to_date,flight_class) VALUES (6,43548,2,6,3,482,87,'2018-05-28 17:30','2018-05-28 08:48','ECONOMY');

INSERT INTO Hotel(pk,company,addr,cost,available,from_date,to_date,amenities_id) VALUES (1,7,1,159,25,'2018-04-20 17:30','2018-05-20 17:30',1);
INSERT INTO Hotel(pk,company,addr,cost,available,from_date,to_date,amenities_id) VALUES (2,8,2,76,10,'2018-04-20 17:30','2018-05-20 17:30',2);

INSERT INTO Location(pk,city,state,country) VALUES (1,'new york city','new york','united states of america');
INSERT INTO Location(pk,city,state,country) VALUES (2,'los angeles','california','united states of america');
INSERT INTO Location(pk,city,state,country) VALUES (3,'boulder','colorado','united states of america');
INSERT INTO Location(pk,city,state,country) VALUES (4,'philadelphia','pennsylvania','united states of america');
INSERT INTO Location(pk,city,state,country) VALUES (5,'boston','massachusetts','united states of america');
INSERT INTO Location(pk,city,state,country) VALUES (6,'seattle','washington','united states of america');
INSERT INTO Location(pk,city,state,country) VALUES (7,'denver','colorado','united states of america');
INSERT INTO Location(pk,city,state,country) VALUES (8,'nassau','new province','bahamas');
INSERT INTO Location(pk,city,state,country) VALUES (9,'king''s wharf','unicorn''s barf','bermuda');
