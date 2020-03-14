#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
from matplotlib import pyplot as plt
import os
from datetime import datetime
import decimal 

#Initialize the app from Flask
app = Flask(__name__)
NUM_TICKET = 100
THRES_TICKET = 0.7
INC_TICKET = decimal.Decimal("1.1")
#Configure MySQL
conn = pymysql.connect(host='127.0.0.1',
                       user='root',
                       password='',
                       db='ticket_reservation',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
	return render_template('index.html')

#Define route for login
@app.route('/login')
def login():
	return render_template('login.html')

#Define route for register index page
@app.route('/register')
def register():
	return render_template('register.html')

#Define route for staff register
@app.route('/staff_register')
def staff_register():
	return render_template('staff_register.html')

#Define route for customer register
@app.route('/customer_register')
def customer_register():
	return render_template('customer_register.html')

#Define route for booking agent register
@app.route('/booking_agent_register')
def booking_agent_register():
	return render_template('booking_agent_register.html')

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	#grabs information from the forms
	#user_type can only be staff/customer/booking_agent
	username = request.form['username']
	password = request.form['password']
	user_type = request.form['user_type']

	valid_type = ["staff","customer","booking_agent"]
	if not (user_type in valid_type):
		#returns an error message to the html page
		error = 'Invalid user type'
		return render_template('login.html', error=error)

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	if user_type == "staff":
		query = 'SELECT * FROM staff WHERE username = %s and password = %s'
		cursor.execute(query, (username, password))
	elif user_type == "customer":
		query = 'SELECT * FROM customer WHERE customer_email = %s and password = %s'
		cursor.execute(query, (username, password))
	elif user_type == "booking_agent":
		query = 'SELECT * FROM booking_agent WHERE agent_email = %s and password = %s'
		cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data and user_type=="staff"):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		session['usertype'] = user_type
		query = 'SELECT airline_name FROM staff WHERE username = %s'
		cursor.execute(query,(username))
		data1 = cursor.fetchone()
		session['airline_name'] = data1['airline_name']
		cursor.close()
		return redirect(url_for('staff_home'))
	elif(data and user_type=="customer"):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		session['usertype'] = user_type
		cursor.close()
		return redirect(url_for('customer_home'))
	elif(data and user_type=="booking_agent"):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		session['usertype'] = user_type
		cursor.close()
		return redirect(url_for('booking_agent_home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		cursor.close()
		return render_template('login.html', error=error)

@app.route('/staff_home')
def staff_home():
    
    username = session['username']
    return render_template('staff_home.html',posts=username)

@app.route('/customer_home')
def customer_home():
    
    username = session['username']
    return render_template('customer_home.html',posts=username)

@app.route('/booking_agent_home')
def booking_agent_home():
    
    username = session['username']
    return render_template('booking_agent_home.html',posts=username)

#Authenticates the register for staff
@app.route('/registerAuths', methods=['GET', 'POST'])
def registerAuths():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']
	permission_code = request.form["permission_code"]
	first_name =  request.form["first_name"]
	last_name = request.form["last_name"]
	date_of_birth = request.form["date_of_birth"]
	airline_name = request.form["airline_name"]

	if permission_code != "staffcode":
		error = "Invalid permission code"
		return render_template('staff_register.html', error = error)
	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query1 = 'SELECT * FROM staff WHERE username = %s'
	cursor.execute(query1, (username))
	#stores the results in a variable
	data1 = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data1):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('staff_register.html', error = error)
	query2 = 'SELECT * from airline where name = %s'
	cursor.execute(query2,(airline_name))
	data2 = cursor.fetchone()
	if(data2 == None):
		error = "The airline doesn't exist"
		return render_template('staff_register.html', error = error)
	else:
		ins = 'INSERT INTO staff VALUES(%s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (username, password, first_name, last_name, date_of_birth, airline_name))
		conn.commit()
		cursor.close()
		return render_template('index.html')

#Authenticates the register for customer
@app.route('/registerAuthc', methods=['GET', 'POST'])
def registerAuthc():
	#grabs information from the forms
	customer_email = request.form["customer_email"]
	password = request.form['password']
	customer_name = request.form["customer_name"]
	building_number = request.form["building_number"]
	street = request.form["street"]
	city = request.form["city"]
	state = request.form["state"]
	phone_number = request.form["phone_number"]
	passport_number = request.form["passport_number"]
	passport_expiration = request.form["passport_expiration"]
	passport_country = request.form["passport_country"]
	date_of_birth = request.form["date_of_birth"]
	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM customer WHERE customer_email = %s'
	cursor.execute(query, (customer_email))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This email already exists"
		return render_template('customer_register.html', error = error)
	else:
		ins = 'INSERT INTO customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (customer_email, customer_name, password, building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country, date_of_birth))
		conn.commit()
		cursor.close()
		return render_template('index.html')

#Authenticates the register for booking agent
@app.route('/registerAuthb', methods=['GET', 'POST'])
def registerAuthb():
	#grabs information from the forms
	agent_email = request.form["agent_email"]
	password = request.form["password"]
	booking_agent_id = request.form["booking_agent_id"]
	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM booking_agent WHERE agent_email = %s'
	cursor.execute(query, (agent_email))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This email already exists"
		return render_template('booking_agent_register.html', error = error)
	else:
		ins = 'INSERT INTO booking_agent VALUES(%s, %s, %s)'
		cursor.execute(ins, (agent_email, password, booking_agent_id))
		conn.commit()
		cursor.close()
		return render_template('index.html')

#public search index without login
@app.route('/public_search_index')
def public_search_index():
	return render_template('public_search_index.html')

#public flight search without login
@app.route('/public_search_result', methods=['GET', 'POST'])
def public_search_result():
	departure_city = request.form["departure_city"]
	arrival_city = request.form["arrival_city"]
	departure_airport = request.form["departure_airport"]
	arrival_airport = request.form["arrival_airport"]
	departure_airport_date = request.form["departure_date"]
	
	if departure_city == "":
		s1 = ''
	else:
		s1 = ' and D.city = \"%s\"' % departure_city
	if arrival_city == "":
		s2 = ''
	else:
		s2 = ' and A.city = \"%s\"' % arrival_city
	if departure_airport == "":
		s3 = ''
	else:
		s3 = ' and F.departure_airport_name = \"%s\"' % departure_airport
	if arrival_airport == "":
		s4 = ''
	else:
		s4 = ' and F.arrival_airport_name = \"%s\"' % arrival_airport
	#print(s1)
	#print(s2)
	
	cursor = conn.cursor();
	query = 'SELECT * FROM flight as F, airport as A, airport as D WHERE D.name = F.departure_airport_name and A.name = F.arrival_airport_name and F.departure_airport_date=%s'
	query = query + s1 + s2 + s3 + s4
	print(query)
	cursor.execute(query,(departure_airport_date))
	data = cursor.fetchall()
	for e in data:
		flight_number = e["flight_number"]
		airline_name = e["airline_name"]
		query1 = 'SELECT count(*) as C FROM ticket as T WHERE T.flight_number = %s and T.airline_name = %s and T.ticket_id not in (SELECT P.ticket_id FROM purchase as P WHERE P.ticket_id = T.ticket_id)'
		cursor.execute(query1, (flight_number,airline_name))
		data1 = cursor.fetchone()
		query2 = 'SELECT base_price FROM flight WHERE flight_number = %s and airline_name = %s'
		cursor.execute(query2, (flight_number,airline_name))
		data2 = cursor.fetchone()
		query3 = 'SELECT count(*) as C FROM ticket WHERE flight_number = %s and airline_name = %s'
		cursor.execute(query3, (flight_number,airline_name))
		data3 = cursor.fetchone()
		num_ticket = data3["C"]
		if data1["C"]/num_ticket < 1 - THRES_TICKET: #data1["C"] is the num of left tickets
			price = data2["base_price"]*INC_TICKET
		else:
			price = data2["base_price"]
		e["price"] = price
    
	return render_template('public_search_result.html',posts = data)

#public flight search for round trip without login
@app.route('/public_round_search_result', methods=['GET', 'POST'])
def public_round_search_result():
	departure_city = request.form["departure_city"]
	arrival_city = request.form["arrival_city"]
	departure_airport = request.form["departure_airport"]
	arrival_airport = request.form["arrival_airport"]
	departure_airport_date = request.form["departure_date"]
	return_date = request.form["return_date"]
	
	if departure_city == "":
		s1 = ''
	else:
		s1 = ' and D.city = \"%s\"' % departure_city
	if arrival_city == "":
		s2 = ''
	else:
		s2 = ' and A.city = \"%s\"' % arrival_city
	if departure_airport == "":
		s3 = ''
	else:
		s3 = ' and F.departure_airport_name = \"%s\"' % departure_airport
	if arrival_airport == "":
		s4 = ''
	else:
		s4 = ' and F.arrival_airport_name = \"%s\"' % arrival_airport
	
	#for return flight
	if departure_city == "":
		s5 = ''
	else:
		s5 = ' and A.city = \"%s\"' % departure_city
	if arrival_city == "":
		s6 = ''
	else:
		s6 = ' and D.city = \"%s\"' % arrival_city
	if arrival_airport == "":
		s7 = ''
	else:
		s7 = ' and F.departure_airport_name = \"%s\"' % arrival_airport
	if departure_airport == "":
		s8 = ''
	else:
		s8 = ' and F.arrival_airport_name = \"%s\"' % departure_airport
	#print(s1)
	#print(s2)
	
	cursor = conn.cursor();
	query = 'SELECT * FROM flight as F, airport as A, airport as D WHERE D.name = F.departure_airport_name and A.name = F.arrival_airport_name and F.departure_airport_date=%s'
	query = query + s1 + s2 + s3 + s4
	print(query)
	cursor.execute(query,(departure_airport_date))
	data = cursor.fetchall()
	for e in data:
		flight_number = e["flight_number"]
		airline_name = e["airline_name"]
		query1 = 'SELECT count(*) as C FROM ticket as T WHERE T.flight_number = %s and T.airline_name = %s and T.ticket_id not in (SELECT P.ticket_id FROM purchase as P WHERE P.ticket_id = T.ticket_id)'
		cursor.execute(query1, (flight_number,airline_name))
		data1 = cursor.fetchone()
		query2 = 'SELECT base_price FROM flight WHERE flight_number = %s and airline_name = %s'
		cursor.execute(query2, (flight_number,airline_name))
		data2 = cursor.fetchone()
		query3 = 'SELECT count(*) as C FROM ticket WHERE flight_number = %s and airline_name = %s'
		cursor.execute(query3, (flight_number,airline_name))
		data3 = cursor.fetchone()
		num_ticket = data3["C"]
		if data1["C"]/num_ticket < 1 - THRES_TICKET: #data1["C"] is the num of left tickets
			price = data2["base_price"]*INC_TICKET
		else:
			price = data2["base_price"]
		e["price"] = price
	#for return flight
	re_query = 'SELECT * FROM flight as F, airport as A, airport as D WHERE D.name = F.departure_airport_name and A.name = F.arrival_airport_name and F.departure_airport_date=%s'
	re_query = re_query + s5 + s6 + s7 + s8
	print(re_query)
	cursor.execute(re_query,(return_date))
	re_data = cursor.fetchall()
	for e in re_data:
		re_flight_number = e["flight_number"]
		re_airline_name = e["airline_name"]
		query1 = 'SELECT count(*) as C FROM ticket as T WHERE T.flight_number = %s and T.airline_name = %s and T.ticket_id not in (SELECT P.ticket_id FROM purchase as P WHERE P.ticket_id = T.ticket_id)'
		cursor.execute(query1, (re_flight_number,re_airline_name))
		data4 = cursor.fetchone()
		query2 = 'SELECT base_price FROM flight WHERE flight_number = %s and airline_name = %s'
		cursor.execute(query2, (re_flight_number,re_airline_name))
		data5 = cursor.fetchone()
		query3 = 'SELECT count(*) as C FROM ticket WHERE flight_number = %s and airline_name = %s'
		cursor.execute(query3, (flight_number,airline_name))
		data6 = cursor.fetchone()
		num_ticket = data6["C"]
		if data4["C"]/num_ticket < 1 - THRES_TICKET: #data1["C"] is the num of left tickets
			price = data5["base_price"]*INC_TICKET
		else:
			price = data5["base_price"]
		e["price"] = price
	cursor.close()
    
	return render_template('public_round_search_result.html',posts = data, re_posts = re_data)

#search index for customer with login
@app.route('/customer_search_index')
def customer_search_index():
	return render_template('customer_search_index.html')

#single search with customer login
@app.route('/customer_search_result', methods=['GET', 'POST'])
def customer_search_result():
	departure_city = request.form["departure_city"]
	arrival_city = request.form["arrival_city"]
	departure_airport = request.form["departure_airport"]
	arrival_airport = request.form["arrival_airport"]
	departure_airport_date = request.form["departure_date"]

	if departure_city == "":
		s1 = ''
	else:
		s1 = ' and D.city = \"%s\"' % departure_city
	if arrival_city == "":
		s2 = ''
	else:
		s2 = ' and A.city = \"%s\"' % arrival_city
	if departure_airport == "":
		s3 = ''
	else:
		s3 = ' and F.departure_airport_name = \"%s\"' % departure_airport
	if arrival_airport == "":
		s4 = ''
	else:
		s4 = ' and F.arrival_airport_name = \"%s\"' % arrival_airport
	#print(s1)
	#print(s2)

	cursor = conn.cursor();
	query = 'SELECT * FROM flight as F, airport as A, airport as D WHERE D.name = F.departure_airport_name and A.name = F.arrival_airport_name and F.departure_airport_date=%s'
	query = query + s1 + s2 + s3 + s4
	print(query)
	cursor.execute(query,(departure_airport_date))
	data = cursor.fetchall()
	for e in data:
		flight_number = e["flight_number"]
		airline_name = e["airline_name"]
		query1 = 'SELECT count(*) as C FROM ticket as T WHERE T.flight_number = %s and T.airline_name = %s and T.ticket_id not in (SELECT P.ticket_id FROM purchase as P WHERE P.ticket_id = T.ticket_id)'
		cursor.execute(query1, (flight_number,airline_name))
		data1 = cursor.fetchone()
		query2 = 'SELECT base_price FROM flight WHERE flight_number = %s and airline_name = %s'
		cursor.execute(query2, (flight_number,airline_name))
		data2 = cursor.fetchone()
		query3 = 'SELECT count(*) as C FROM ticket WHERE flight_number = %s and airline_name = %s'
		cursor.execute(query3, (flight_number,airline_name))
		data3 = cursor.fetchone()
		num_ticket = data3["C"]
		if data1["C"]/num_ticket < 1 - THRES_TICKET: #data1["C"] is the num of left tickets
			price = data2["base_price"]*INC_TICKET
		else:
			price = data2["base_price"]
		e["price"] = price
	cursor.close()
    
	return render_template('customer_search_result.html',posts = data)

#round search with customer log in
@app.route('/customer_round_search_result', methods=['GET', 'POST'])
def customer_round_search_result():
 departure_city = request.form["departure_city"]
 arrival_city = request.form["arrival_city"]
 departure_airport = request.form["departure_airport"]
 arrival_airport = request.form["arrival_airport"]
 departure_airport_date = request.form["departure_date"]
 return_date = request.form["return_date"]
 
 if departure_city == "":
  s1 = ''
 else:
  s1 = ' and D.city = \"%s\"' % departure_city
 if arrival_city == "":
  s2 = ''
 else:
  s2 = ' and A.city = \"%s\"' % arrival_city
 if departure_airport == "":
  s3 = ''
 else:
  s3 = ' and F.departure_airport_name = \"%s\"' % departure_airport
 if arrival_airport == "":
  s4 = ''
 else:
  s4 = ' and F.arrival_airport_name = \"%s\"' % arrival_airport
 
 #for return flight
 if departure_city == "":
  s5 = ''
 else:
  s5 = ' and A.city = \"%s\"' % departure_city
 if arrival_city == "":
  s6 = ''
 else:
  s6 = ' and D.city = \"%s\"' % arrival_city
 if arrival_airport == "":
  s7 = ''
 else:
  s7 = ' and F.departure_airport_name = \"%s\"' % arrival_airport
 if departure_airport == "":
  s8 = ''
 else:
  s8 = ' and F.arrival_airport_name = \"%s\"' % departure_airport
 #print(s1)
 #print(s2)
 cursor = conn.cursor();
 query = 'SELECT * FROM flight as F, airport as A, airport as D WHERE D.name = F.departure_airport_name and A.name = F.arrival_airport_name and F.departure_airport_date=%s'
 query = query + s1 + s2 + s3 + s4
 print(query)
 cursor.execute(query,(departure_airport_date))
 data = cursor.fetchall()
 for e in data:
  flight_number = e["flight_number"]
  airline_name = e["airline_name"]
  query1 = 'SELECT count(*) as C FROM ticket as T WHERE T.flight_number = %s and T.airline_name = %s and T.ticket_id not in (SELECT P.ticket_id FROM purchase as P WHERE P.ticket_id = T.ticket_id)'
  cursor.execute(query1, (flight_number,airline_name))
  data1 = cursor.fetchone()
  query2 = 'SELECT base_price FROM flight WHERE flight_number = %s and airline_name = %s'
  cursor.execute(query2, (flight_number,airline_name))
  data2 = cursor.fetchone()
  query3 = 'SELECT count(*) as C FROM ticket WHERE flight_number = %s and airline_name = %s'
  cursor.execute(query3, (flight_number,airline_name))
  data3 = cursor.fetchone()
  num_ticket = data3["C"]
  if data1["C"]/num_ticket < 1 - THRES_TICKET: #data1["C"] is the num of left tickets
   price = data2["base_price"]*INC_TICKET
  else:
   price = data2["base_price"]
  e["price"] = price
 #for return flight
 re_query = 'SELECT * FROM flight as F, airport as A, airport as D WHERE D.name = F.departure_airport_name and A.name = F.arrival_airport_name and F.departure_airport_date=%s'
 re_query = re_query + s5 + s6 + s7 + s8
 print(re_query)
 cursor.execute(re_query,(return_date))
 re_data = cursor.fetchall()
 for e in re_data:
  re_flight_number = e["flight_number"]
  re_airline_name = e["airline_name"]
  query1 = 'SELECT count(*) as C FROM ticket as T WHERE T.flight_number = %s and T.airline_name = %s and T.ticket_id not in (SELECT P.ticket_id FROM purchase as P WHERE P.ticket_id = T.ticket_id)'
  cursor.execute(query1, (re_flight_number,re_airline_name))
  data3 = cursor.fetchone()
  query2 = 'SELECT base_price FROM flight WHERE flight_number = %s and airline_name = %s'
  cursor.execute(query2, (re_flight_number,re_airline_name))
  data4 = cursor.fetchone()
  query3 = 'SELECT count(*) as C FROM ticket WHERE flight_number = %s and airline_name = %s'
  cursor.execute(query3, (flight_number,airline_name))
  data5 = cursor.fetchone()
  num_ticket = data5["C"]
  if data3["C"]/num_ticket < 1 - THRES_TICKET: #data1["C"] is the num of left tickets
   re_price = data4["base_price"]*INC_TICKET
  else:
   re_price = data4["base_price"]
  e["re_price"] = re_price
 cursor.close()
 return render_template('customer_round_search_result.html',posts = data, re_posts = re_data)


 #search index for booking agent with login
@app.route('/agent_search_index')
def agent_search_index():
	return render_template('agent_search_index.html')

#single search with booking agent login
@app.route('/agent_search_result', methods=['GET', 'POST'])
def agent_search_result():
 departure_city = request.form["departure_city"]
 arrival_city = request.form["arrival_city"]
 departure_airport = request.form["departure_airport"]
 arrival_airport = request.form["arrival_airport"]
 departure_airport_date = request.form["departure_date"]
 
 if departure_city == "":
  s1 = ''
 else:
  s1 = ' and D.city = \"%s\"' % departure_city
 if arrival_city == "":
  s2 = ''
 else:
  s2 = ' and A.city = \"%s\"' % arrival_city
 if departure_airport == "":
  s3 = ''
 else:
  s3 = ' and F.departure_airport_name = \"%s\"' % departure_airport
 if arrival_airport == "":
  s4 = ''
 else:
  s4 = ' and F.arrival_airport_name = \"%s\"' % arrival_airport
 #print(s1)
 #print(s2)
 
 cursor = conn.cursor();
 query = 'SELECT * FROM flight as F, airport as A, airport as D WHERE D.name = F.departure_airport_name and A.name = F.arrival_airport_name and F.departure_airport_date=%s'
 query = query + s1 + s2 + s3 + s4
 print(query)
 cursor.execute(query,(departure_airport_date))
 data = cursor.fetchall()
 for e in data:
  flight_number = e["flight_number"]
  airline_name = e["airline_name"]
  query1 = 'SELECT count(*) as C FROM ticket as T WHERE T.flight_number = %s and T.airline_name = %s and T.ticket_id not in (SELECT P.ticket_id FROM purchase as P WHERE P.ticket_id = T.ticket_id)'
  cursor.execute(query1, (flight_number,airline_name))
  data1 = cursor.fetchone()
  query2 = 'SELECT base_price FROM flight WHERE flight_number = %s and airline_name = %s'
  cursor.execute(query2, (flight_number,airline_name))
  data2 = cursor.fetchone()
  query3 = 'SELECT count(*) as C FROM ticket WHERE flight_number = %s and airline_name = %s'
  cursor.execute(query3, (flight_number,airline_name))
  data3 = cursor.fetchone()
  num_ticket = data3["C"]
  if data1["C"]/num_ticket < 1 - THRES_TICKET: #data1["C"] is the num of left tickets
   price = data2["base_price"]*INC_TICKET
  else:
   price = data2["base_price"]
  e["price"] = price
 cursor.close()
    
 return render_template('agent_search_result.html',posts = data)

#round search with booking agent log in
@app.route('/agent_round_search_result', methods=['GET', 'POST'])
def agent_round_search_result():
 departure_city = request.form["departure_city"]
 arrival_city = request.form["arrival_city"]
 departure_airport = request.form["departure_airport"]
 arrival_airport = request.form["arrival_airport"]
 departure_airport_date = request.form["departure_date"]
 return_date = request.form["return_date"]
 
 if departure_city == "":
  s1 = ''
 else:
  s1 = ' and D.city = \"%s\"' % departure_city
 if arrival_city == "":
  s2 = ''
 else:
  s2 = ' and A.city = \"%s\"' % arrival_city
 if departure_airport == "":
  s3 = ''
 else:
  s3 = ' and F.departure_airport_name = \"%s\"' % departure_airport
 if arrival_airport == "":
  s4 = ''
 else:
  s4 = ' and F.arrival_airport_name = \"%s\"' % arrival_airport
 
 #for return flight
 if departure_city == "":
  s5 = ''
 else:
  s5 = ' and A.city = \"%s\"' % departure_city
 if arrival_city == "":
  s6 = ''
 else:
  s6 = ' and D.city = \"%s\"' % arrival_city
 if arrival_airport == "":
  s7 = ''
 else:
  s7 = ' and F.departure_airport_name = \"%s\"' % arrival_airport
 if departure_airport == "":
  s8 = ''
 else:
  s8 = ' and F.arrival_airport_name = \"%s\"' % departure_airport
 #print(s1)
 #print(s2)
 cursor = conn.cursor();
 query = 'SELECT * FROM flight as F, airport as A, airport as D WHERE D.name = F.departure_airport_name and A.name = F.arrival_airport_name and F.departure_airport_date=%s'
 query = query + s1 + s2 + s3 + s4
 print(query)
 cursor.execute(query,(departure_airport_date))
 data = cursor.fetchall()
 for e in data:
  flight_number = e["flight_number"]
  airline_name = e["airline_name"]
  query1 = 'SELECT count(*) as C FROM ticket as T WHERE T.flight_number = %s and T.airline_name = %s and T.ticket_id not in (SELECT P.ticket_id FROM purchase as P WHERE P.ticket_id = T.ticket_id)'
  cursor.execute(query1, (flight_number,airline_name))
  data1 = cursor.fetchone()
  query2 = 'SELECT base_price FROM flight WHERE flight_number = %s and airline_name = %s'
  cursor.execute(query2, (flight_number,airline_name))
  data2 = cursor.fetchone()
  query3 = 'SELECT count(*) as C FROM ticket WHERE flight_number = %s and airline_name = %s'
  cursor.execute(query3, (flight_number,airline_name))
  data3 = cursor.fetchone()
  num_ticket = data3["C"]
  if data1["C"]/num_ticket < 1 - THRES_TICKET: #data1["C"] is the num of left tickets
   price = data2["base_price"]*INC_TICKET
  else:
   price = data2["base_price"]
  e["price"] = price
 #for return flight
 re_query = 'SELECT * FROM flight as F, airport as A, airport as D WHERE D.name = F.departure_airport_name and A.name = F.arrival_airport_name and F.departure_airport_date=%s'
 re_query = re_query + s5 + s6 + s7 + s8
 print(re_query)
 cursor.execute(re_query,(return_date))
 re_data = cursor.fetchall()
 for e in re_data:
  re_flight_number = e["flight_number"]
  re_airline_name = e["airline_name"]
  query1 = 'SELECT count(*) as C FROM ticket as T WHERE T.flight_number = %s and T.airline_name = %s and T.ticket_id not in (SELECT P.ticket_id FROM purchase as P WHERE P.ticket_id = T.ticket_id)'
  cursor.execute(query1, (re_flight_number,re_airline_name))
  data3 = cursor.fetchone()
  query2 = 'SELECT base_price FROM flight WHERE flight_number = %s and airline_name = %s'
  cursor.execute(query2, (re_flight_number,re_airline_name))
  data4 = cursor.fetchone()
  query3 = 'SELECT count(*) as C FROM ticket WHERE flight_number = %s and airline_name = %s'
  cursor.execute(query3, (flight_number,airline_name))
  data5 = cursor.fetchone()
  num_ticket = data5["C"]
  if data3["C"]/num_ticket < 1 - THRES_TICKET: #data1["C"] is the num of left tickets
   re_price = data4["base_price"]*INC_TICKET
  else:
   re_price = data4["base_price"]
  e["re_price"] = re_price
 cursor.close()
    
 return render_template('agent_round_search_result.html',posts = data, re_posts = re_data)


@app.route('/purchaseAuth/<airline_name>/<flight_number>/<price>', methods=['GET', 'POST'])
def purchase(airline_name,flight_number,price):
 username = session['username']
 #save the price of that flight into cookie
 session['price'] = price
 cursor = conn.cursor();
    #find a ticket from the given flight_number & airline_name
 query = 'SELECT * FROM ticket natural join flight WHERE flight_number = %s and airline_name = %s and ticket_id not in (SELECT P.ticket_id FROM purchase as P WHERE P.ticket_id = ticket_id)'
 cursor.execute(query, (flight_number,airline_name))
 data = cursor.fetchone()
 print(data)
 if data == None:
  return render_template('purchase_index.html', message="sold_out")
 session['ticket_id'] = data["ticket_id"]
 session['flight_number'] = data["flight_number"]
 session['airline_name'] = data["airline_name"]
 conn.commit()
 cursor.close()
 return render_template('purchase_index.html', username=username, posts=data, price=price)


#purchase time/date is inserted automatically by default value
@app.route('/purchase_commit', methods=['GET', 'POST'])
def purchase_commit():
	price = session['price']
	usertype = session['usertype']
	ticket_id = session['ticket_id']
	cursor = conn.cursor()
	if usertype == "customer":
		agent_email = "dummy" #for customer, the agent email is empty
		username = session['username']

		query2 = 'SELECT * FROM booking_agent where agent_email = %s'
		dummy = 'dummy'
		cursor.execute(query2,(dummy))
		data2 = cursor.fetchone()
		if (data2 == None):
			query3 = 'INSERT INTO booking_agent (agent_email, password, booking_agent_id) values(%s,%s,%s)'
			cursor.execute(query3,(dummy, dummy, dummy))
			conn.commit()
	else:
		agent_email = session['username'] #for agent
		username = request.form['customer_email']
	card_type = request.form['card_type']
	card_number = request.form['card_number']
	card_name = request.form['card_name']
	expiration_date = request.form['expiration_date']
	#expiration_str = str(expiration_date)
	#print(type(price))
	query1 = 'INSERT INTO purchase (ticket_id,customer_email,agent_email,card_type,card_number,card_name,expiration_date,sold_price) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'
	cursor.execute(query1, (ticket_id,username,agent_email,card_type,card_number,card_name,expiration_date,price))
	#print(query % (ticket_id,username,agent_email,card_type,card_number,card_name,expiration_date,price,))
	conn.commit()
	cursor.close()
	flight_number = session['flight_number']
	airline_name = session['airline_name']
	if usertype == "customer":
		return render_template('purchase_success_c.html', ticket_id=ticket_id,flight_number=flight_number,airline_name=airline_name, price=price)
	else:
		return render_template('purchase_success_b.html', ticket_id=ticket_id,flight_number=flight_number,airline_name=airline_name, price=price)

@app.route('/flight_status')
def flight_status():
	return render_template('flight_status.html')

#public flight search without login
@app.route('/status_result', methods=['GET', 'POST'])
def status_result():
	flight_number = request.form["flight_number"]
	airline_name = request.form["airline_name"]
	departure_airport_date = request.form["departure_date"]
	arrival_airport_date = request.form["arrival_date"]
	
	if airline_name == "":
		s1 = ''
	else:
		s1 = ' and airline_name = \"%s\"' % airline_name
	if departure_airport_date == "":
		s2 = ''
	else:
		s2 = ' and departure_airport_date = \"%s\"' % departure_airport_date
	if arrival_airport_date == "":
		s3 = ''
	else:
		s3 = ' and arrival_airport_date = \"%s\"' % arrival_airport_date
	#print(s1)
	#print(s2)
	
	cursor = conn.cursor();
	query = 'SELECT * FROM flight WHERE flight_number = %s'
	query = query + s1 + s2 + s3
	print(query)
	cursor.execute(query,(flight_number))
	data = cursor.fetchall()
	cursor.close()
    
	return render_template('status_result.html',posts = data)















#------------------customer---------------------#
#4. View my flights
@app.route('/customer_view_flight',methods=['GET','POST'])
def customer_view_flight():
 customer_email = session['username']
 cursor = conn.cursor()
 query = 'SELECT * FROM flight natural join ticket natural join purchase where departure_airport_date >= NOW() AND customer_email = %s'
 cursor.execute(query, (customer_email))
 data = cursor.fetchall()
 conn.commit()
 cursor.close()
 return render_template('customer_view_flight.html', posts=data)

#5. Search for flights
@app.route('/customer_flight_search', methods=['POST'])
def customer_flight_search():
 customer_email = session['username']
 arrival_airport_name = request.form['arrival_airport_name']
 departure_airport_name = request.form['departure_airport_name']
 departure_airport_date = request.form['departure_airport_date']
 query = 'SELECT * FROM flight natural join ticket natural join purchase WHERE customer_email = %s and arrival_airport_name = %s and departure_airport_name = %s and departure_airport_date = %s'
 cursor = conn.cursor()
 cursor.execute(query, (customer_email, arrival_airport_name, departure_airport_name, departure_airport_date))
 data = cursor.fetchall()
 conn.commit()
 cursor.close()
 return render_template('optional_customer_flight_search.html', posts=data)

#7. Track my Spending:
@app.route('/customer_view_spending',methods=['GET','POST'])
def customer_view_spending():
	customer_email = session['username']
	cursor = conn.cursor()
	#show all future flights
	query = 'SELECT customer_email, sum(sold_price) as total_spending from purchase where customer_email = %s and purchase_ts <= NOW() and purchase_ts > NOW() - INTERVAL 1 YEAR'
	cursor.execute(query, (customer_email))
	data = cursor.fetchone()
	conn.commit()
	month_data = []
	for i in range(6):
		query = 'SELECT customer_email, sum(sold_price) as monthly_spending FROM purchase where customer_email = %s and purchase_ts >= NOW() - INTERVAL %s MONTH AND purchase_ts < NOW() - INTERVAL %s MONTH'
		cursor.execute(query, (customer_email, i+1, i))
		temp_data = cursor.fetchone()
		month_data.append(temp_data)
	cursor.close()
	month_spend = []
	time_line = []
	for i in range(len(month_data)):
		temp_spend = month_data[len(month_data)-i-1]['monthly_spending']
		if temp_spend == None:
			temp_spend = 0
		else:
			temp_spend = float(temp_spend)
		month_spend.append(temp_spend)
		time_line.append(i+1)
	print(month_spend)
	print(time_line)
	plt.clf()
	plt.bar(time_line, month_spend, align='center', alpha=0.5)
	plt.xlabel('time period')
	plt.ylabel('spending')
	plt.title('month wise spending of last 6 months')
	basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
	imgdir = '/static/customer_spend.png'
	file_path = basedir + imgdir
	plt.savefig(file_path,dpi=400)
	end_date = datetime.today().strftime('%Y-%m-%d')
	return render_template('customer_view_spending.html', posts=data, month_spend=month_spend, end_date=end_date)

@app.route('/customer_view_spending_optional', methods=['POST'])
def customer_view_spending_optional():
	customer_email = session['username']
	start_date = request.form['start_date']
	end_date = request.form['end_date']
	cursor = conn.cursor()
	query = 'SELECT customer_email, sum(sold_price) as total_spending from purchase where customer_email = %s and purchase_ts >= %s and purchase_ts <= %s'
	cursor.execute(query, (customer_email,start_date, end_date))
	data = cursor.fetchone()
	conn.commit()
	month_data = []
	end_date_l = end_date.split("-")
	start_date_l = start_date.split("-")
	num_month = (int(end_date_l[0]) - int(start_date_l[0])) * 12 + int(end_date_l[1]) - int(start_date_l[1]) + 1
	print(num_month)
	for i in range(num_month):
		query = 'SELECT customer_email, sum(sold_price) as monthly_spending FROM purchase where customer_email = %s and purchase_ts >= %s - INTERVAL %s MONTH AND purchase_ts < %s - INTERVAL %s MONTH'
		cursor.execute(query, (customer_email, end_date,i+1, end_date,i))
		temp_data = cursor.fetchone()
		month_data.append(temp_data)
	conn.commit()
	cursor.close()
	month_spend = []
	time_line = []
	for i in range(len(month_data)):
		temp_spend = month_data[len(month_data)-i-1]['monthly_spending']
		if temp_spend == None:
			temp_spend = 0
		else:
			temp_spend = float(temp_spend)
		month_spend.append(temp_spend)
		time_line.append(i+1)
	print(month_spend)
	print(time_line)
	plt.clf()
	plt.bar(time_line, month_spend, align='center', alpha=0.5)
	plt.xlabel('time period')
	plt.ylabel('spending')
	plt.title('month wise spending')
	basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
	imgdir = '/static/customer_spend_optional.png'
	file_path = basedir + imgdir
	plt.savefig(file_path,dpi=400)

	return render_template('customer_view_spending_optional.html', posts=data, end_date=end_date, month_spend=month_spend)










#------------------Airline staff----------------#
#4. View my Flights:
@app.route('/staff_view_flight',methods=['GET','POST'])
def staff_view_flight():
	username = session['username']
	cursor = conn.cursor()
	query1 = 'SELECT airline_name FROM staff where username = %s'
	cursor.execute(query1,(username))
	data1 = cursor.fetchone()
	airline_name = data1['airline_name']
	query2 = 'SELECT * FROM flight where airline_name = %s and departure_airport_date >= NOW() AND departure_airport_date < NOW() + INTERVAL 1 MONTH'
	cursor.execute(query2, (airline_name))
	data2 = cursor.fetchall()
	conn.commit()
	cursor.close()
	return render_template('staff_view_flight.html', posts=data2)

@app.route('/staff_flight_search', methods=['POST'])
def staff_flight_search():
	username = session['username']
	arrival_airport_name = request.form['arrival_airport_name']
	departure_airport_name = request.form['departure_airport_name']
	departure_airport_date = request.form['departure_airport_date']
	cursor = conn.cursor()
	query1 = 'SELECT airline_name FROM staff where username = %s'
	cursor.execute(query1,(username))
	data1 = cursor.fetchone()
	airline_name = data1['airline_name']
	query = 'SELECT * FROM flight WHERE airline_name = %s and arrival_airport_name = %s and departure_airport_name = %s and departure_airport_date = %s'
	cursor = conn.cursor()
	cursor.execute(query, (airline_name, arrival_airport_name, departure_airport_name, departure_airport_date))
	data = cursor.fetchall()
	conn.commit()
	cursor.close()
	return render_template('optional_staff_flight_search.html', posts=data)

#5. Create new flights:
@app.route('/staff_add_flight_index',methods=['GET','POST'])
def staff_add_flight_index():
	return render_template('staff_add_flight.html')

@app.route('/staff_add_flight_default',methods=['GET','POST'])
def staff_add_flight_default():
	username = session['username']
	cursor = conn.cursor()
	query1 = 'SELECT airline_name FROM staff where username = %s'
	cursor.execute(query1,(username))
	data1 = cursor.fetchone()
	airline_name = data1['airline_name']
	query2 = 'SELECT * FROM flight where airline_name = %s and departure_airport_date >= NOW() AND departure_airport_date < NOW() + INTERVAL 1 MONTH'
	cursor.execute(query2, (airline_name))
	data2 = cursor.fetchall()
	conn.commit()
	cursor.close()
	return render_template('staff_add_flight_default.html', posts=data2)

@app.route('/staff_add_flight',methods=['GET','POST'])
def staff_add_flight():
	username = session['username']
	flight_number = request.form["flight_number"]
	airline_name = request.form["airline_name"]
	airplane_id = request.form["airplane_id"]
	departure_airport_name = request.form["departure_airport_name"]
	arrival_airport_name = request.form["arrival_airport_name"]
	departure_airport_date = request.form["departure_airport_date"]
	departure_airport_time = request.form["departure_airport_time"]
	arrival_airport_date = request.form["arrival_airport_date"]
	arrival_airport_time = request.form["arrival_airport_time"]
	base_price = request.form["base_price"]
	status = request.form["status"]
	cursor = conn.cursor();
	query4 = 'SELECT * FROM flight WHERE flight_number = %s and airline_name = %s'
	cursor.execute(query4,(flight_number,airline_name))
	data4 = cursor.fetchone()
	error = None
	if (data4):
		# if the flight already exists, return error
		error = "This flight already exists"
		return render_template('staff_add_flight.html',error = error)
	else:
		query7 = 'SELECT airline_name FROM staff WHERE username = %s'
		cursor.execute(query7, (username))
		data7 = cursor.fetchone()
		error = None
		if(airline_name != data7['airline_name']):
			error = "You are not authorized to add flights of other airlines"
			return render_template('staff_add_flight.html',error = error)
		else:
			query1 = 'SELECT * FROM airplane WHERE airline_name = %s AND airplane_id = %s'
			cursor.execute(query1, (airline_name,airplane_id))
			data1 = cursor.fetchone()
			query2 = 'SELECT * FROM airport WHERE name = %s'
			cursor.execute(query2, (departure_airport_name))
			data2 = cursor.fetchone()
			query3 = 'SELECT * FROM airport WHERE name = %s'
			cursor.execute(query3, (arrival_airport_name))
			data3 = cursor.fetchone()
			error = None
			if((data1!=None) and (data2!=None) and (data3!=None)):
				query5 = 'INSERT INTO flight VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
				cursor.execute(query5, (flight_number,airline_name,base_price,arrival_airport_name,departure_airport_name,arrival_airport_time, arrival_airport_date, departure_airport_time,departure_airport_date,airplane_id,status))
				print(query5)
				#get number of seats for the flight
				query6 = 'SELECT seats FROM airplane where airplane_id = %s and airline_name = %s'
				cursor.execute(query6, (airplane_id,airline_name))
				data6 = cursor.fetchone()
				#automatically generate tickets for all the seats
				for i in range(data6['seats']):
					ticket_id = airline_name + flight_number + str(i)
					query = 'INSERT INTO ticket (ticket_id, flight_number, airline_name) VALUES (%s, %s, %s)'
					cursor.execute(query, (ticket_id, flight_number, airline_name))
				conn.commit()
				cursor.close()
				return redirect(url_for('staff_home'))
			else:
				#if any of the result returns null, gives an error
				error = "Please validate your new flight beforehand"
				return render_template('staff_add_flight.html',error = error)

#6. Change status of flights:
@app.route('/staff_update_status_index',methods=['GET','POST'])
def staff_update_status_index():
	return render_template('staff_update_status.html')

@app.route('/staff_update_status',methods=['GET','POST'])
def staff_update_status():
	username = session['username']
	flight_number = request.form["flight_number"]
	airline_name = request.form["airline_name"]
	status = request.form["status"]
	cursor = conn.cursor()
	query1 = 'SELECT * FROM flight WHERE flight_number = %s AND airline_name = %s'
	cursor.execute(query1,(flight_number,airline_name))
	data1 = cursor.fetchone()
	error = None
	if (not data1):
		#if the flight doesn't exist, return error
		error = "This flight doesn't exist. Try again."
		return render_template('staff_update_status.html', error = error)
	else:
		query4 = 'SELECT airline_name FROM staff WHERE username = %s'
		cursor.execute(query4, (username))
		data4 = cursor.fetchone()
		error = None
		if(airline_name != data4['airline_name']):
			error = "You are not authorized to update flight status of other airlines"
			return render_template('staff_update_status.html',error = error)
		query2 = 'UPDATE flight SET status = %s WHERE flight_number = %s AND airline_name = %s'
		cursor.execute(query2,(status,flight_number,airline_name))
	conn.commit()
	cursor.close()
	return redirect(url_for('staff_home'))

#7. add airplane in the system:
@app.route('/staff_add_airplane_index',methods=['GET','POST'])
def staff_add_airplane_index():
	return render_template('staff_add_airplane.html')

@app.route('/staff_add_airplane',methods=['GET','POST'])
def staff_add_airplane():
	username = session['username']
	airplane_id = request.form["airplane_id"]
	airline_name = request.form["airline_name"]
	seats = request.form["seats"]
	cursor = conn.cursor();
	query1 = 'SELECT * FROM airplane WHERE airplane_id = %s AND airline_name = %s'
	cursor.execute(query1,(airplane_id, airline_name))
	data1 = cursor.fetchone()
	error = None
	if (data1):
		#if the airplane already exists, return error
		error = "This airplane already exists"
		return render_template('staff_add_airplane.html',error = error)
	else:
		#check the foreign key constraint
		query2 = 'SELECT * FROM airline WHERE name = %s'
		cursor.execute(query2, (airline_name))
		data2 = cursor.fetchone()
		query4 = 'SELECT airline_name FROM staff WHERE username = %s'
		cursor.execute(query4, (username))
		data4 = cursor.fetchone()
		error = None
		if(airline_name != data4['airline_name']):
			error = "You are not authorized to add airplanes of other airlines"
			return render_template('staff_add_airplane.html',error = error)
		elif(data2 == None):
			#if any of the result returns null, gives an error
			error = "Please validate your new airplane beforehand"
			return render_template('staff_add_airplane.html',error = error)
		else:
			query3 = 'INSERT INTO airplane (airplane_id,airline_name,seats) VALUES (%s, %s, %s)'
			cursor.execute(query3,(airplane_id,airline_name,seats))
	conn.commit()
	cursor.close()
	return redirect(url_for('staff_add_airplane_confirmation'))

@app.route('/staff_add_airplane_confirmation',methods=['GET','POST'])
def staff_add_airplane_confirmation():
	username = session['username']
	cursor = conn.cursor()
	query1 = 'SELECT airline_name FROM staff WHERE username = %s'
	cursor.execute(query1, (username))
	data1 = cursor.fetchone()
	airline_name = data1['airline_name']
	query2 = 'SELECT * FROM airplane WHERE airline_name = %s'
	cursor.execute(query2,(airline_name))
	data2 = cursor.fetchall()
	conn.commit()
	cursor.close()
	return render_template('staff_add_airplane_confirmation_result.html',posts = data2)

#8. add new airport in the system:
@app.route('/staff_add_airport_index',methods=['GET','POST'])
def staff_add_airport_index():
	return render_template('staff_add_airport.html')

@app.route('/staff_add_airport',methods=['GET','POST'])
def staff_add_airport():
	name = request.form["name"]
	city = request.form["city"]
	cursor = conn.cursor();
	query1 = 'SELECT * FROM airport WHERE name = %s'
	cursor.execute(query1,(name))
	data1 = cursor.fetchone()
	error = None
	if (data1):
		#if the airport name already exists, return error
		error = "This airport already exists"
		return render_template('staff_add_airport.html',error = error)
	else:
		query2 = 'INSERT INTO airport(name, city) VALUES (%s, %s)'
		cursor.execute(query2, (name, city))
	conn.commit()
	cursor.close()
	return redirect(url_for('staff_home'))

#9. view booking agents:
@app.route('/staff_view_agent_index',methods=['GET','POST'])
def staff_view_agent_index():
	return render_template('staff_view_agent.html')

@app.route('/staff_view_agent',methods=['GET','POST'])
def staff_view_agent():
	method = request.form['method']
	cursor = conn.cursor()
	error = None
	if method == 'past one month':
		query1 = 'SELECT agent_email, count(*) AS count FROM purchase where agent_email <> "dummy" AND purchase_ts <= NOW() AND purchase_ts > NOW() - INTERVAL 1 MONTH GROUP BY agent_email ORDER BY count DESC LIMIT 5'
		cursor.execute(query1, ())
		data1 = cursor.fetchall()
		return render_template('staff_view_agent_result.html', posts = data1)
	elif method == 'past one year':
		query2 = 'SELECT agent_email, count(*) AS count FROM purchase where agent_email <> "dummy" AND purchase_ts <= NOW() AND purchase_ts > NOW() - INTERVAL 1 YEAR GROUP BY agent_email ORDER BY count DESC LIMIT 5'
		cursor.execute(query2, ())
		data2 = cursor.fetchall()
		return render_template('staff_view_agent_result.html', posts = data2)
	elif method == 'commission':
		query3 = 'SELECT agent_email, sum(sold_price * 0.1) AS count FROM purchase where agent_email <> "dummy" AND purchase_ts <= NOW() AND purchase_ts > NOW() - INTERVAL 1 YEAR GROUP BY agent_email ORDER BY count DESC LIMIT 5'
		cursor.execute(query3, ())
		data3 = cursor.fetchall()
		return render_template('staff_view_agent_result.html', posts = data3)
	else:
		error = 'Please clarify your method & method can only be chosen from "one month" or "one year" or "commission"! '
		return render_template('staff_view_agent.html', error = error)
	conn.commit()
	cursor.close()
	return redirect(url_for('staff_home'))

#10. view frequent customers:
@app.route('/staff_view_customer_index',methods=['GET','POST'])
def staff_view_customer_index():
	return redirect(url_for('staff_view_customer'))

@app.route('/staff_view_customer',methods=['GET','POST'])
def staff_view_customer():
	username = session['username']
	cursor = conn.cursor()
	query1 = 'SELECT airline_name FROM staff WHERE username = %s'
	cursor.execute(query1,(username))
	data1 = cursor.fetchone()
	error = None
	if (data1 == None):
		error = 'No airline found. Please check your username.'
		return render_template('staff_home.html', error = error)
	else:
		airline_name = data1['airline_name']
		query2 = 'DROP VIEW IF EXISTS customer_view'
		cursor.execute(query2,())
		query3 = 'CREATE VIEW customer_view AS SELECT customer_email, COUNT(flight_number) AS num FROM purchase NATURAL JOIN ticket WHERE airline_name = %s GROUP BY customer_email'
		cursor.execute(query3,(airline_name))
		query4 = 'SELECT distinct customer_email, flight_number FROM purchase NATURAL JOIN ticket WHERE airline_name = %s AND customer_email in (SELECT customer_email FROM customer_view WHERE num = (SELECT MAX(num) FROM customer_view))'
		cursor.execute(query4,(airline_name))
		data4 = cursor.fetchall()
		if (data4 == None):
			error = 'No flight_number found. Error!'
			return render_template('staff_home.html', error = error)
		else:
			return render_template('staff_view_customer_result.html', posts = data4)
		conn.commit()
		cursor.close()
		return redirect(url_for('staff_home'))

#11. view reports

#12. comparison of revenue earned
@app.route('/staff_view_revenue_index',methods=['GET','POST'])
def staff_view_revenue_index():
	return redirect(url_for('staff_view_revenue'))

@app.route('/staff_view_revenue',methods=['GET','POST'])
def staff_view_revenue():
	cursor = conn.cursor()
	#for past month no booking agent
	query1 = 'SELECT sum(sold_price) as revenue FROM purchase natural join ticket WHERE airline_name = %s and agent_email = "dummy" AND purchase_ts <= NOW() AND purchase_ts > NOW() - INTERVAL 1 MONTH'
	cursor.execute(query1,(session['airline_name']))
	data1 = cursor.fetchone()
	#for past month with booking agent
	query2 = 'SELECT sum(sold_price) as revenue FROM purchase natural join ticket WHERE airline_name = %s and agent_email <> "dummy" AND purchase_ts <= NOW() AND purchase_ts > NOW() - INTERVAL 1 MONTH'
	cursor.execute(query2,(session['airline_name']))
	data2 = cursor.fetchone()

	dir_sale = data1['revenue']
	indir_sale = data2['revenue']
	if dir_sale == None:
		dir_sale = 0
	else:
		dir_sale = float(data1['revenue'])
	if indir_sale == None:
		indir_sale = 0
	else:
		indir_sale = float(data2['revenue'])
	dir_sale1 = 100*dir_sale/(dir_sale+indir_sale)
	indir_sale1 = 100*indir_sale/(dir_sale+indir_sale)
	labels = ["direct_sale", "indirect_sale"]
	sizes = [dir_sale,indir_sale]
	explode = [0,0.1]
	fig1, ax1 = plt.subplots()
	ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
	ax1.axis('equal')
	plt.title('dir_sale/indir_sale percentage')
	basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
	imgdir = '/static/month_dir_sale_percent.png'
	file_path = basedir + imgdir
	plt.savefig(file_path,dpi=400)
	#for past year no booking agent
	query3 = 'SELECT sum(sold_price) as revenue FROM purchase natural join ticket WHERE airline_name = %s and agent_email = "dummy" AND purchase_ts <= NOW() AND purchase_ts > NOW() - INTERVAL 1 YEAR'
	cursor.execute(query3,(session['airline_name']))
	data3 = cursor.fetchone()
	query4 = 'SELECT sum(sold_price) as revenue FROM purchase natural join ticket WHERE airline_name = %s and agent_email <> "dummy" AND purchase_ts <= NOW() AND purchase_ts > NOW() - INTERVAL 1 YEAR'
	cursor.execute(query4,(session['airline_name']))
	data4 = cursor.fetchone()
	conn.commit()
	dir_sale = data3['revenue']
	indir_sale = data4['revenue']
	if dir_sale == None:
		dir_sale = 0
	else:
		dir_sale = float(data3['revenue'])
	if indir_sale == None:
		indir_sale = 0
	else:
		indir_sale = float(data4['revenue'])
	dir_sale2 = 100*dir_sale/(dir_sale+indir_sale)
	indir_sale2 = 100*indir_sale/(dir_sale+indir_sale)
	labels = ["direct_sale", "indirect_sale"]
	sizes = [dir_sale,indir_sale]
	explode = [0,0.1]
	fig1, ax1 = plt.subplots()
	ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
	ax1.axis('equal')
	plt.title('dir_sale/indir_sale percentage')
	basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
	imgdir = '/static/year_dir_sale_percent.png'
	file_path = basedir + imgdir
	plt.savefig(file_path,dpi=400)
	cursor.close()
	return render_template('staff_view_revenue_result.html', data1 = data1, data2 = data2, data3 = data3, data4 = data4, dir_sale1=dir_sale1, indir_sale1=indir_sale1, dir_sale2=dir_sale2, indir_sale2=indir_sale2)

#13. view top destinations
@app.route('/staff_view_destination_index', methods = ['GET', 'POST'])
def staff_view_destination_index():
	return redirect(url_for('staff_view_destination'))

@app.route('/staff_view_destination', methods = ['GET','POST'])
def staff_view_destination():
	cursor = conn.cursor()
	#for past three months
	query1 = 'SELECT airport.city as name, count(*) AS count FROM purchase NATURAL JOIN ticket NATURAL JOIN flight, airport WHERE airline_name = %s AND airport.name = arrival_airport_name AND purchase_ts <= NOW() AND purchase_ts > NOW() - INTERVAL 3 MONTH GROUP BY arrival_airport_name ORDER BY count DESC LIMIT 3'
	cursor.execute(query1,(session['airline_name']))
	data1 = cursor.fetchall()
	#for past year
	query2 = 'SELECT airport.city as name, count(*) AS count FROM purchase NATURAL JOIN ticket NATURAL JOIN flight, airport WHERE airline_name = %s AND airport.name = arrival_airport_name AND purchase_ts <= NOW() AND purchase_ts > NOW() - INTERVAL 1 YEAR GROUP BY arrival_airport_name ORDER BY count DESC LIMIT 3'
	cursor.execute(query2,(session['airline_name']))
	data2 = cursor.fetchall()
	conn.commit()
	cursor.close()
	return render_template('staff_view_destination_result.html', data1 = data1, data2 = data2)

@app.route('/staff_view_reports', methods = ['GET','POST'])
def staff_view_reports():
	cursor = conn.cursor()
	#for past month ticket sold
	query1 = 'SELECT count(*) as num_t FROM purchase natural join ticket WHERE airline_name = %s AND purchase_ts <= NOW() AND purchase_ts > NOW() - INTERVAL 1 MONTH'
	cursor.execute(query1,(session['airline_name']))
	data1 = cursor.fetchone()

	month_ticket_sale = data1['num_t']
	end_date = datetime.today().strftime('%Y-%m-%d')

	ticket_sale = [data1['num_t']]
	time_line = [1]
	plt.clf()
	plt.bar(time_line, ticket_sale, align='center', alpha=0.5)
	plt.xlabel('time')
	plt.ylabel('number_of_ticket_bought')
	plt.title('last month ticket sale')
	basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
	imgdir = '/static/month_reports.png'
	file_path = basedir + imgdir
	plt.savefig(file_path,dpi=400)
	
	#for past year ticket sold
	query2 = 'SELECT count(*) as num_t FROM purchase natural join ticket WHERE airline_name = %s AND purchase_ts <= NOW() AND purchase_ts > NOW() - INTERVAL 1 YEAR'
	cursor.execute(query2,(session['airline_name']))
	data2 = cursor.fetchone()
	conn.commit()
	
	#monthly ticket sold bar chart for last year 
	month_data = []
	time_line = []
	for i in range(12):
		query = 'SELECT count(*) as num_t FROM purchase natural join ticket where airline_name = %s and purchase_ts >= NOW() - INTERVAL %s MONTH AND purchase_ts < NOW() - INTERVAL %s MONTH'
		cursor.execute(query, (session['airline_name'], i+1, i))
		temp_data = cursor.fetchone()
		month_data.append(temp_data['num_t'])
		time_line.append(11-i)
	conn.commit()
	plt.clf()
	plt.bar(time_line, month_data, align='center', alpha=0.5)
	plt.xlabel('time')
	plt.ylabel('number_of_ticket_bought')
	plt.title('last year ticket sale')
	basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
	imgdir = '/static/year_reports.png'
	file_path = basedir + imgdir
	plt.savefig(file_path,dpi=400)
	cursor.close()
	return render_template('staff_view_reports_result.html', data1 = data1, data2 = data2, end_date=end_date, month_ticket_sale=month_ticket_sale, year_ticket_sale=month_data)

@app.route('/staff_view_reports_optional', methods = ['GET','POST'])
def staff_view_reports_optional():	
	start_date = request.form['start_date']
	end_date = request.form['end_date']
	cursor = conn.cursor()
	query = 'SELECT count(*) as num_t from purchase natural join ticket where airline_name = %s and purchase_ts >= %s and purchase_ts <= %s'
	cursor.execute(query, (session['airline_name'],start_date, end_date))
	data1 = cursor.fetchone()
	conn.commit()

	end_date_l = end_date.split("-")
	start_date_l = start_date.split("-")
	num_month = (int(end_date_l[0]) - int(start_date_l[0])) * 12 + int(end_date_l[1]) - int(start_date_l[1]) + 1
	print(num_month)
	#monthly ticket sold bar chart for last year 
	month_data = []
	time_line = []
	for i in range(num_month):
		query = 'SELECT count(*) as num_t FROM purchase natural join ticket where airline_name = %s and purchase_ts >= %s - INTERVAL %s MONTH AND purchase_ts < %s - INTERVAL %s MONTH'
		cursor.execute(query, (session['airline_name'],end_date, i+1,end_date, i))
		temp_data = cursor.fetchone()
		month_data.append(temp_data['num_t'])
		time_line.append(num_month-i)
	conn.commit()
	plt.clf()
	plt.bar(time_line, month_data, align='center', alpha=0.5)
	plt.xlabel('time')
	plt.ylabel('number_of_ticket_bought')
	plt.title('month wise ticket sale')
	basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
	imgdir = '/static/month_wise_reports.png'
	file_path = basedir + imgdir
	plt.savefig(file_path,dpi=400)
	cursor.close()
	return render_template('staff_view_reports_optional.html', data1 = data1, end_date=end_date, month_spend=month_data)










#-----------------booking agent----------------------#
#4. View my flights
@app.route('/agent_view_flight',methods=['GET','POST'])
def agent_view_flight():
	agent_email = session['username']
	cursor = conn.cursor()
	#show all future flights
	query = 'SELECT customer_email, ticket_id, flight_number, airline_name, arrival_airport_name, arrival_airport_date, arrival_airport_time, departure_airport_name, departure_airport_date, departure_airport_time, status FROM flight natural join ticket natural join purchase where departure_airport_date >= NOW() and agent_email = %s'
	cursor.execute(query, (agent_email))
	data = cursor.fetchall()
	conn.commit()
	cursor.close()
	return render_template('agent_view_flight.html', posts=data)

@app.route('/agent_view_flight_optional', methods=['POST'])
def agent_view_flight_optional():
	agent_email = session['username']
	departure_airport_name = request.form['departure_airport_name']
	arrival_airport_name = request.form['arrival_airport_name']
	departure_airport_date = request.form['departure_airport_date']
	arrival_airport_date = request.form['arrival_airport_date']
	cursor = conn.cursor()
	query = 'SELECT customer_email, ticket_id, flight_number, airline_name, arrival_airport_name, arrival_airport_date, arrival_airport_time, departure_airport_name, departure_airport_date, departure_airport_time, status FROM flight natural join ticket natural join purchase where agent_email = %s and departure_airport_name = %s and arrival_airport_name = %s and departure_airport_date >= %s and arrival_airport_date<= %s '
	cursor.execute(query, (agent_email,departure_airport_name,arrival_airport_name,departure_airport_date,arrival_airport_date))
	data = cursor.fetchall()
	conn.commit()
	cursor.close()
	return render_template('agent_view_flight_optional_result.html', posts=data)

#5. Search for flights
#6. Purchase tickets
#7. View my commission
@app.route('/agent_view_commission',methods=['GET','POST'])
def agent_view_commission():
	agent_email = session['username']
	cursor = conn.cursor()
	#show all future flights
	query = 'SELECT agent_email, sum(sold_price * 0.1) as total_commission, sum(sold_price*0.1)/count(ticket_id) as average_commission, count(ticket_id) as tickets_sold from purchase where agent_email = %s and purchase_ts <= NOW() and purchase_ts > NOW() - INTERVAL 1 MONTH'
	cursor.execute(query, (agent_email))
	data = cursor.fetchone()
	conn.commit()
	cursor.close()
	return render_template('agent_view_commission.html', posts=data)

@app.route('/agent_view_commission_optional', methods=['POST'])
def agent_view_commission_optional():
	agent_email = session['username']
	start_date = request.form['start_date']
	end_date = request.form['end_date']
	cursor = conn.cursor()
	query = 'SELECT agent_email, sum(sold_price * 0.1) as total_commission, sum(sold_price*0.1)/count(ticket_id) as average_commission, count(ticket_id) as tickets_sold from purchase where agent_email = %s and purchase_ts >= %s and purchase_ts <= %s '
	cursor.execute(query, (agent_email,start_date, end_date))
	data = cursor.fetchone()
	conn.commit()
	cursor.close()
	return render_template('agent_view_commission_optional_result.html', posts=data)

#8. View Top Customers
@app.route('/agent_view_customer_index',methods=['GET','POST'])
def agent_view_customer_index():
	return redirect(url_for('agent_view_customer'))

@app.route('/agent_view_customer',methods=['GET','POST'])
def agent_view_customer():
	agent_email = session['username']
	cursor = conn.cursor()
	#top 5 customers based on number of tickets sold in the past 6 months
	query1 = 'SELECT customer_email, count(*) AS tickets_sold FROM purchase where agent_email = %s AND purchase_ts <= NOW() AND purchase_ts > NOW() - INTERVAL 6 MONTH GROUP BY customer_email ORDER BY tickets_sold DESC LIMIT 5'
	cursor.execute(query1,(agent_email))
	data1 = cursor.fetchall()
	#top 5 customers based on amount of commissions received in the past year
	query2 = 'SELECT customer_email, sum(sold_price * 0.1) AS total_commission FROM purchase where agent_email = %s AND purchase_ts <= NOW() AND purchase_ts > NOW() - INTERVAL 1 YEAR GROUP BY customer_email ORDER BY total_commission DESC LIMIT 5'
	cursor.execute(query2,(agent_email))
	data2 = cursor.fetchall()
	conn.commit()
	cursor.close()

	if (data1 == None or data2 == None):
		error = 'You have not purchased tickets for customers yet! '
		return render_template('booking_agent_home.html', error = error)
	else:
		customer_name = []
		customer_spend = []
		for i in range(len(data1)):
			temp_spend = data1[i]['tickets_sold']
			if temp_spend == None:
				temp_spend = 0
			customer_spend.append(temp_spend)
			customer_name.append(i+1)
		plt.bar(customer_name, customer_spend, align='center', alpha=0.5)
		plt.xlabel('customer_name')
		plt.ylabel('number_of_ticket_bought')
		plt.title('top 5 customers based on number of ticket bought')
		basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
		imgdir = '/static/top5_c_ticket.png'
		file_path = basedir + imgdir
		plt.savefig(file_path,dpi=400)

		customer_name = []
		customer_spend = []
		for i in range(len(data2)):
			temp_spend = data2[i]['total_commission']
			if temp_spend == None:
				temp_spend = 0
			customer_spend.append(temp_spend)
			customer_name.append(i+1)
		plt.bar(customer_name, customer_spend, align='center', alpha=0.5)
		plt.xlabel('customer_name')
		plt.ylabel('total_commission')
		plt.title('top 5 customers based on total commissions')
		basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
		imgdir = '/static/top5_c_commission.png'
		file_path = basedir + imgdir
		plt.savefig(file_path,dpi=400)
		return render_template('agent_view_customer_result.html', data1 = data1, data2 = data2)

@app.route('/logout')
def logout():
	session.pop('username')
	session.clear()
	return redirect('/')

app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)