CREATE TABLE "travel_agency_address" (
	"address_id" integer NOT NULL PRIMARY KEY, 
	"line1" varchar(50) NOT NULL, 
	"line2" varchar(50) NOT NULL, 
	"city" varchar(35) NOT NULL, 
	"state" varchar(2) NOT NULL, 
	"country" varchar(50) NOT NULL, 
	"zip_code" integer NOT NULL
)

CREATE TABLE "travel_agency_amenities" (
	"amenities_id" integer NOT NULL PRIMARY KEY, 
	"breakfast" bool NOT NULL, 
	"internet" bool NOT NULL, 
	"parking" bool NOT NULL, 
	"fitness" bool NOT NULL, 
	"pool" bool NOT NULL, 
	"bar" bool NOT NULL
)

CREATE TABLE "travel_agency_car" ("number" varchar(5) NOT NULL, "cost" integer NOT NULL, "available" integer NOT NULL, "car_id" integer NOT NULL PRIMARY KEY, "confirmation_id" integer NOT NULL, "car_class" varchar(10) NOT NULL, "company_id" integer NOT NULL REFERENCES "travel_agency_company" ("company_id") DEFERRABLE INITIALLY DEFERRED, "from_date" datetime NOT NULL, "to_date" datetime NOT NULL, "from_location_id" integer NOT NULL REFERENCES "travel_agency_location" ("location_id") DEFERRABLE INITIALLY DEFERRED, "to_location_id" integer NOT NULL REFERENCES "travel_agency_location" ("location_id") DEFERRABLE INITIALLY DEFERRED)

CREATE TABLE "travel_agency_company" ("company_id" integer NOT NULL PRIMARY KEY, "name" varchar(256) NOT NULL)

CREATE TABLE "travel_agency_cruise" ("number" varchar(5) NOT NULL, "cost" integer NOT NULL, "available" integer NOT NULL, "cruise_id" integer NOT NULL PRIMARY KEY, "company_id" integer NOT NULL REFERENCES "travel_agency_company" ("company_id") DEFERRABLE INITIALLY DEFERRED, "from_date" datetime NOT NULL, "to_date" datetime NOT NULL, "from_location_id" integer NOT NULL REFERENCES "travel_agency_location" ("location_id") DEFERRABLE INITIALLY DEFERRED, "to_location_id" integer NOT NULL REFERENCES "travel_agency_location" ("location_id") DEFERRABLE INITIALLY DEFERRED)

CREATE TABLE "travel_agency_flight" ("number" varchar(5) NOT NULL, "cost" integer NOT NULL, "available" integer NOT NULL, "flight_id" integer NOT NULL PRIMARY KEY, "flight_class" varchar(10) NOT NULL, "company_id" integer NOT NULL REFERENCES "travel_agency_company" ("company_id") DEFERRABLE INITIALLY DEFERRED, "from_location_id" integer NOT NULL REFERENCES "travel_agency_location" ("location_id") DEFERRABLE INITIALLY DEFERRED, "to_location_id" integer NOT NULL REFERENCES "travel_agency_location" ("location_id") DEFERRABLE INITIALLY DEFERRED, "from_date" datetime NOT NULL, "to_date" datetime NOT NULL)

CREATE TABLE "travel_agency_hotel" (
	"hotel_id" integer NOT NULL PRIMARY KEY, 
	"number" varchar(5) NOT NULL, 
	"available" integer NOT NULL, 
	"cost" integer NOT NULL, 
	"addr_id" integer NOT NULL UNIQUE REFERENCES "travel_agency_address" ("address_id") DEFERRABLE INITIALLY DEFERRED, 
	"amenities_id" integer NOT NULL UNIQUE REFERENCES "travel_agency_amenities" ("amenities_id") DEFERRABLE INITIALLY DEFERRED, 
	"company_id" integer NOT NULL REFERENCES "travel_agency_company" ("company_id") DEFERRABLE INITIALLY DEFERRED, 
	"location_id" integer NOT NULL UNIQUE REFERENCES "travel_agency_location" ("location_id") DEFERRABLE INITIALLY DEFERRED, 
	"from_date" datetime NOT NULL, "to_date" datetime NOT NULL
)

CREATE TABLE "travel_agency_location" (
	"location_id" integer NOT NULL PRIMARY KEY, 
	"city" varchar(35) NOT NULL, 
	"state" varchar(2) NULL, 
	"country" varchar(254) NOT NULL
)

CREATE TABLE "travel_agency_payment" ("payment_id" integer NOT NULL PRIMARY KEY, "credit_no" integer NOT NULL, "expiry" date NOT NULL)

CREATE TABLE "travel_agency_profile" ("profile_id" integer NOT NULL PRIMARY KEY, "first_name" varchar(20) NOT NULL, "last_name" varchar(20) NOT NULL, "email" varchar(254) NOT NULL, "billing_addr_id" integer NULL UNIQUE REFERENCES "travel_agency_address" ("address_id") DEFERRABLE INITIALLY DEFERRED, "home_addr_id" integer NULL UNIQUE REFERENCES "travel_agency_address" ("address_id") DEFERRABLE INITIALLY DEFERRED, "payment_method_id" integer NULL REFERENCES "travel_agency_payment" ("payment_id") DEFERRABLE INITIALLY DEFERRED, "user_id_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED)

CREATE TABLE "travel_agency_review" ("review_id" integer NOT NULL PRIMARY KEY, "content" varchar(256) NOT NULL, "rating" integer NOT NULL, "date" date NOT NULL, "company_id_id" integer NOT NULL REFERENCES "travel_agency_company" ("company_id") DEFERRABLE INITIALLY DEFERRED, "user_id_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED)

CREATE TABLE "travel_agency_search" ("search_id" integer NOT NULL PRIMARY KEY, "user_id" integer NOT NULL, "from_date" date NOT NULL, "to_date" date NULL, "travelers_count" integer NOT NULL, "from_location_id" integer NOT NULL REFERENCES "travel_agency_location" ("location_id") DEFERRABLE INITIALLY DEFERRED, "to_location_id" integer NULL REFERENCES "travel_agency_location" ("location_id") DEFERRABLE INITIALLY DEFERRED)

CREATE TABLE "travel_agency_travel" ("travel_id" integer NOT NULL PRIMARY KEY, "user_id" integer NOT NULL, "payment_id" integer NOT NULL, "travel_date" date NOT NULL, "from_location_id" integer NOT NULL REFERENCES "travel_agency_location" ("location_id") DEFERRABLE INITIALLY DEFERRED, "to_location_id" integer NOT NULL REFERENCES "travel_agency_location" ("location_id") DEFERRABLE INITIALLY DEFERRED)