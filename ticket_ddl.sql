create table airline (
	name VARCHAR(25) PRIMARY KEY
);

#multi valued attributes phone_number is stored in seperate table
create table staff (
	username VARCHAR(50) PRIMARY KEY,
	password VARCHAR(50),
	first_name VARCHAR(25),
	last_name VARCHAR(25),
	date_of_birth DATE,
	airline_name VARCHAR(25),
	FOREIGN KEY (airline_name) REFERENCES airline(name) ON DELETE SET NULL
);

#phone number for staff
create table phone_number (
	phone VARCHAR(20),
	staff_username VARCHAR(50),
	PRIMARY KEY (phone, staff_username),
	FOREIGN KEY (staff_username) REFERENCES staff(username) ON DELETE CASCADE
);

#contain the info of airline and relation owns
create table airplane (
	airline_name VARCHAR(25),
	airplane_id VARCHAR(50),
	seats int,
	PRIMARY KEY (airline_name,airplane_id),
	FOREIGN KEY (airline_name) REFERENCES airline(name) ON DELETE CASCADE
);

create table airport (
	name VARCHAR(25) PRIMARY KEY,
	city VARCHAR(25)
);

#the status of flight can be computed by arrival time
#contain the info of airport-flight relation, airline-flight relation
#airplane-flight relation
create table flight (
	flight_number VARCHAR(25),
	airline_name VARCHAR(25),
	base_price DECIMAL(8,2),
	arrival_airport_name VARCHAR(25),
	departure_airport_name VARCHAR(25),
	arrival_airport_time time,
	arrival_airport_date DATE,
	departure_airport_time time,
	departure_airport_date DATE,
	airplane_id VARCHAR(50),
	status VARCHAR(25) DEFAULT "On Time",
	PRIMARY KEY (airline_name,flight_number),
	FOREIGN KEY (arrival_airport_name) REFERENCES airport(name) ON DELETE CASCADE,
	FOREIGN KEY (departure_airport_name) REFERENCES airport(name) ON DELETE CASCADE,
	FOREIGN KEY (airline_name,airplane_id) REFERENCES airplane(airline_name,airplane_id) ON DELETE CASCADE
);

#composite attribute payment_info is splitted into several attributes
create table ticket (
	ticket_id VARCHAR(50) PRIMARY KEY,
	flight_number VARCHAR(25),
	airline_name VARCHAR(25),
	FOREIGN KEY (airline_name,flight_number) REFERENCES flight(airline_name,flight_number) ON DELETE CASCADE
);

create table booking_agent (
	agent_email VARCHAR(50) PRIMARY KEY,
	password VARCHAR(50),
	booking_agent_id VARCHAR(50)
);

create table customer (
	customer_email VARCHAR(50) PRIMARY KEY,
	customer_name VARCHAR(50),
	password VARCHAR(50),
	building_number VARCHAR(25),
	street VARCHAR(25),
	city VARCHAR(25),
	state VARCHAR(5),
	phone_number VARCHAR(25),
	passport_number VARCHAR(25),
	passport_expiration DATE,
	passport_country VARCHAR(10),
	date_of_birth DATE
);

#relation between customer, booking agent, and ticket
create table purchase (
	ticket_id VARCHAR(50),
	customer_email VARCHAR(50),
	agent_email VARCHAR(50),
	card_type VARCHAR(25),
	card_number VARCHAR(25),
	card_name VARCHAR(25),
	expiration_date DATE,
	purchase_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	sold_price DECIMAL(8,2),
	PRIMARY KEY (ticket_id, customer_email, agent_email),
	FOREIGN KEY (ticket_id) REFERENCES ticket(ticket_id) ON DELETE CASCADE,
	FOREIGN KEY (customer_email) REFERENCES customer(customer_email) ON DELETE CASCADE,
	FOREIGN KEY (agent_email) REFERENCES booking_agent(agent_email) ON DELETE CASCADE
);



