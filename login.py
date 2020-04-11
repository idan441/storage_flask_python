from flask import Flask, session, redirect, url_for, escape, request
import logging #For the abillity to add logs in the terminal
import db_conn
app = Flask(__name__)



conn = db_conn.db_conn()#Sets a connection to DB object. 


#Login and logout functions used by main page - 
def login(username, password):
	print(username, password)
	print("SELECT u_id, d_name, is_active, is_admin FROM users WHERE u_name = '%s' AND password = '%s' " % (username, password))
	username_details = conn.select_query_single_row("SELECT u_id, d_name, is_active, is_admin FROM users WHERE u_name = '%s' AND password = '%s' " % (username, password))
	if(username_details == False): #If username and password were not found
		logging.warn("wrong attempt to login - username %s , password %s " % (username, password) )
		return False

	#If login succeded - check if the user is active
	if(username_details[2] == 0): #If is_active = 0 = false
		return False

	#Else, start setting the sessions: 
	session['u_id'] = username_details[0] #The user id which will be used in the db to relate the user to it's actions. 
	session['d_name'] = username_details[1] #The name of the user, that will be presented in the rendered pages. 
	session['is_admin'] = username_details[3] #For actions which requires admin premissions. 

	return True

def logout():
	session.pop('u_id', None)
	session.pop('d_name', None) 
	session.pop('is_admin', None)
	return True


#Functions used to access user details, by other pages - 
def get_user_id(u_id): 
	pass

def get_user_name(u_id): 
	pass

def is_user_admin(u_id): 
	pass

def is_user_active(u_id): 
	pass

