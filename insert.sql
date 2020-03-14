INSERT INTO airline(name)
VALUES ("China Eastern");
	
INSERT INTO airport(name,city)
VALUES ("JFK","NYC");

INSERT INTO airport(name,city)
VALUES ("PVG","Shanghai");

INSERT INTO customer(customer_email,customer_name,password,building_number,
	street,city,state,phone_number,passport_number,passport_expiration,passport_country,
	date_of_birth)
VALUES ("rg2971@nyu.edu","Robin","123456","01","Century Avenue","Shanghai",
	"Shanghai","13967134708","N14530918","2025-08-15","China",
	"1997-09-01");

INSERT INTO customer(customer_email,customer_name,password,building_number,
	street,city,state,phone_number,passport_number,passport_expiration,passport_country,
	date_of_birth)
VALUES ("yz2821@nyu.edu","Cathy","123456","01","Century Avenue","Shanghai",
	"Shanghai","13967134708","N14530918","2025-08-15","China",
	"1997-07-26");

INSERT INTO airplane(airline_name,airplane_id,seats)
VALUES ("China Eastern","0123",100)

INSERT INTO airplane(airline_name,airplane_id,seats)
VALUES ("China Eastern","0246",150)

INSERT INTO staff(username,password,first_name,last_name,date_of_birth,airline_name)
VALUES ("RobinGong","012345","Ruoming","Gong","1997-09-01","China Eastern")

INSERT INTO flight(airline_name,flight_number,base_price,arrival_airport_name,
	departure_airport_name,arrival_airport_time,arrival_airport_date,
	departure_airport_time,departure_airport_date,airplane_id,status)
VALUES ("China Eastern","CE1097",10000.00,"JFK","PVG","17:30","2019-01-29","13:30",
	"2019-01-29","0123","On Time")

INSERT INTO flight(airline_name,flight_number,base_price,arrival_airport_name,
	departure_airport_name,arrival_airport_time,arrival_airport_date,
	departure_airport_time,departure_airport_date,airplane_id,status)
VALUES ("China Eastern","CE2048",10000.00,"JFK","PVG","17:30","2019-01-30","13:30",
	"2019-01-30","0123","Delayed")

INSERT INTO booking_agent(agent_email,password,booking_agent_id)
VALUES ("bookingagent@gmail.com","000000","000001")

INSERT INTO booking_agent(agent_email,password,booking_agent_id)
VALUES ("dummy",null,null)

INSERT INTO ticket(ticket_id,flight_number,airline_name)
VALUES ("001234","CE1097","China Eastern")

INSERT INTO ticket(ticket_id,flight_number,airline_name)
VALUES ("004321","CE1097","China Eastern")

INSERT INTO purchase(ticket_id,customer_email,agent_email,card_type,card_number,
	card_name,expiration_date,sold_price)
VALUES ("001234","rg2971@nyu.edu","dummy","visa","00000000","GONG RUOMING","1997-09-01",10000.00)

INSERT INTO purchase(ticket_id,customer_email,agent_email,card_type,card_number,
	card_name,expiration_date,sold_price)
VALUES ("004321","rg2971@nyu.edu","bookingagent@gmail.com","visa","00000000","GONG RUOMING","1997-09-01",10000.00)



