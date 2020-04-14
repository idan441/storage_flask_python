#!/bin/python
import db_conn


#This page has translation functions. These functions accept an ID of a record from the database AND returns a textual detailed string about this id. 


conn = db_conn.db_conn() #Set the connection to the database, this will be used by the following functions. 


#Users table related functions: 
def get_user_u_name(user_id):
	u_name = conn.select_query_single_row("SELECT u_name FROM users WHERE u_id = '%s' " % (user_id))
	if (u_name == False): 
		return "wrong id - no username"
	return u_name[0]

def get_user_d_name(user_id):
	result = conn.select_query_single_row("SELECT d_name FROM users WHERE u_id = '%s' " % (user_id))
	if (result == False): 
		return "wrong id - no display name"
	return result[0]

def get_user_is_active(user_id):
	result = conn.select_query_single_row("SELECT is_active FROM users WHERE u_id = '%s' " % (user_id))
	if (result == False): 
		return "wrong id - unable to locate whether user is active"
	return result[0]

def get_user_is_admin(user_id):
	result = conn.select_query_single_row("SELECT is_admin FROM users WHERE u_id = '%s' " % (user_id))
	if (result == False): 
		return "wrong id - unable to locate whether user is admin"
	return result[0]



#Warehouses table related functions: 




#Items table related functions: 




#Transactions table related functions: 
def translate_status(status_code):
	#Translates the status id of a transaction - to its title. 
	#transactions statuses - created (1) , open (2) , finished (3) , canceled (4) , deleted (5) 
	status_dictionary = {1:'created', 2:'open', 3:'finished', 4:'canceled', 5:'deleted'}
	if(status_code in status_dictionary):
		return status_dictionary[status_code] + ("(%s)" % (status_code))
	else:
		return "wrong status code"

def transalte_transaction_type(transaction_type):
	#Translates the transaction_type of a transaction - to its title. 
	#transactions statuses - deposit (1) , withdraw (2)
	status_dictionary = {1:'deposit', 2:'withdraw'}
	if(transaction_type in status_dictionary):
		return status_dictionary[transaction_type] + ("(%s)" % (transaction_type))
	else:
		return "wrong transaction type"

