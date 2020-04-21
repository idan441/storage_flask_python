from flask import Flask, session, redirect, url_for, escape, request
import logging #For the abillity to add logs in the terminal
import sys #Allows to use the exit() function to abort the code. 
import db_conn


conn = db_conn.db_conn()#Sets a connection to DB object. 



#Login and logout functions used by main page - 
def login(username, password):
	username_details = conn.select_query_single_row("SELECT u_id, d_name, is_active, is_admin FROM users WHERE u_name = '%s' AND password = '%s' " % (username, password))
	if(username_details == False): #If username and password were not found
		logging.warn("wrong attempt to login - username %s , password %s " % (str(username), str(password)) )
		return False

	#If login succeded - check if the user is active
	if(username_details[2] == 0): #If is_active = 0 = false
		logging.warn("An unactivated user tried to log in - username %s" % (str(username)) )
		return False

	#Else, start setting the sessions: 
	session['u_id'] = username_details[0] #The user id which will be used in the db to relate the user to it's actions. 
	session['d_name'] = username_details[1] #The name of the user, that will be presented in the rendered pages. 
	session['is_admin'] = username_details[3] #For actions which requires admin premissions. 
	logging.info("Login to the system - user %s" % (str(username)) )

	return True

def logout():
	session.pop('u_id', None)
	session.pop('d_name', None) 
	session.pop('is_admin', None)
	return True

def is_logged_in():
	if('u_id' in session):
		return 1
	return 0

def is_logged_in_admin():
	if('u_id' in session and session['is_admin'] == 1):
		return 1
	return 0


#Functions used to access user's session details, by other pages - 
def get_u_id(): 
	if(session.get("u_id") is not None): 
		return session['u_id']
	logging.error("asked for u_id but this session is not exist")
	exit("asked for user session details while no user is loged in! function name get_user_id()") 

def get_d_name(): 
	if(session.get('d_name') is not None): 
		return session['d_name']
	logging.error("asked for d_name but this session is not exist")
	exit("asked for user session details while no user is loged in! function name get_d_name()") 

def get_is_admin(): 
	if(session.get('is_admin') is not None): 
		return session['is_admin']
	logging.error("asked for is_admin but this session is not exist")
	exit("asked for user session details while no user is loged in! function name get_is_admin()") 
