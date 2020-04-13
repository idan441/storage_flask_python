#!/bin/python
import db_conn


#This page has translation functions. These functions accept an ID of a record from the database AND returns a textual detailed string about this id. 


conn = db_conn.db_conn() #Set the connection to the database, this will be used by the following functions. 


#Users table related functions: 
def get_user_u_name(user_id):
	result = conn.select_query_single_row("SELECT u_name FROM users WHERE u_id = %s" % (user_id))
	if (result == False): 
		return "wrong id - no username"
	return result[0]

def get_user_d_name(user_id):
	result = conn.select_query_single_row("SELECT d_name FROM users WHERE u_id = %s" % (user_id))
	if (result == False): 
		return "wrong id - no display name"
	return result[0]

def get_user_is_active(user_id):
	result = conn.select_query_single_row("SELECT is_active FROM users WHERE u_id = %s" % (user_id))
	if (result == False): 
		return "wrong id - unable to locate whether user is active"
	return result[0]

def get_user_is_admin(user_id):
	result = conn.select_query_single_row("SELECT is_admin FROM users WHERE u_id = %s" % (user_id))
	if (result == False): 
		return "wrong id - unable to locate whether user is admin"
	return result[0]



#Warehouses table related functions: 




#Items table related functions: 




#Transactions table related functions: 





