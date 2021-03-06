#!/bin/python
import db_conn


#This page has translation functions. These functions accept an ID of a record from the database AND returns a textual detailed string about this id. 


conn = db_conn.db_conn() #Set the connection to the database, this will be used by the following functions. 


#Users table related functions: 
def get_user_u_name(user_id):
	u_name = conn.select_query_single_row("SELECT u_name FROM users WHERE u_id = '%s' " % (user_id))
	if (u_name == False): 
		return "wrong id - no username" + str(user_id)
	return u_name[0]

def get_user_d_name(user_id):
	if(user_id == None):
		return "User not set"
	result = conn.select_query_single_row("SELECT d_name FROM users WHERE u_id = '%s' " % (user_id))
	if (result == False): 
		return "wrong id - no display name" + str(user_id)
	return result[0]

def get_user_is_active(user_id):
	result = conn.select_query_single_row("SELECT is_active FROM users WHERE u_id = '%s' " % (user_id))
	if (result == False): 
		return "wrong id - unable to locate whether user is active" + str(user_id)
	return result[0]

def get_user_is_admin(user_id):
	result = conn.select_query_single_row("SELECT is_admin FROM users WHERE u_id = '%s' " % (user_id))
	if (result == False): 
		return "wrong id - unable to locate whether user is admin" + str(user_id)
	return result[0]



#Warehouses table related functions: 
def get_warehouse_name(wh_id):
	result = conn.select_query_single_row("SELECT wh_name FROM warehouses WHERE wh_id = '%s' " % (wh_id))
	if (result == False): 
		return "Warehouse not exist"
	return result[0]

def is_warehouse_active(wh_id):
	result = conn.select_query_single_row("SELECT is_active FROM warehouses WHERE wh_id = '%s' " % (wh_id))
	if (result == False): 
		return "Warehouse not exist"
	return result[0]



#Items table related functions: 
def get_item_name(item_id):
	result = conn.select_query_single_row("SELECT item_name FROM items WHERE item_id = '%s' " % (item_id))
	if (result == False): 
		return "item not exist"
	return result[0]

def get_item_amount(item_id):
	result = conn.select_query_single_row("SELECT amount FROM items WHERE item_id = '%s' " % (item_id))
	if (result == False): 
		return "item not exist"
	return result[0]

def get_item_m_unit(item_id):
	result = conn.select_query_single_row("SELECT m_unit FROM items WHERE item_id = '%s' " % (item_id))
	if (result == False): 
		return "item not exist"
	return result[0]

def get_item_amount_with_m_unit(item_id):
	result = conn.select_query_single_row("SELECT amount, m_unit FROM items WHERE item_id = '%s' " % (item_id))
	if (result == False): 
		return "item not exist"
	return str(result[0]) + " " + str(result[1])




#Traders table related functions: 
def get_trader_name(t_id):
	if(t_id == None):
		return "No trader set"

	trader = conn.select_query_single_row("SELECT t_name, t_id FROM traders WHERE t_id = '%s' " % (t_id))
	if (trader == False): 
		return "trader not exist"
	return str(trader[0])

def is_trader_active(t_id):
	trader = conn.select_query_single_row("SELECT is_active FROM traders WHERE t_id = '%s' " % (t_id))
	if (trader == False): 
		return "trader not exist"
	return trader[0]

def is_trader_supplier(t_id):
	trader = conn.select_query_single_row("SELECT is_supplier FROM traders WHERE t_id = '%s' " % (t_id))
	if (trader == False): 
		return "trader not exist"
	return trader[0]

def is_trader_costumer(t_id):
	trader = conn.select_query_single_row("SELECT is_costumer FROM traders WHERE t_id = '%s' " % (t_id))
	if (trader == False): 
		return "trader not exist"
	return trader[0]





#Transactions functions: 
def get_transaction_type(t_id):
	result = conn.select_query_single_row("SELECT transaction_type FROM transactions WHERE transaction_id = '%s' " % (t_id))
	if (result == False): 
		return "transaction not found! transaction id " + str(t_id)
	return result[0]

def get_transaction_title(t_id):
	result = conn.select_query_single_row("SELECT title FROM transactions WHERE transaction_id = '%s' " % (t_id))
	if (result == False): 
		return "transaction not found! transaction id " + str(t_id)
	return result[0]

def get_transaction_status(t_id):
	result = conn.select_query_single_row("SELECT status FROM transactions WHERE transaction_id = '%s' " % (t_id))
	if (result == False): 
		return "transaction not found! transaction id " + str(t_id)
	return result[0]




#Transactions table related functions: 
def translate_status(status_code):
	#Translates the status id of a transaction - to its title. 
	#transactions statuses - created (1) , open (2) , finished (3) , canceled (4) , deleted (5) 
	status_dictionary = {1:'created', 2:'open', 3:'finished', 4:'canceled', 5:'deleted'}
	if(status_code in status_dictionary):
		return status_dictionary[status_code] + ("(%s)" % (status_code))
	else:
		return "wrong status code" + str(status_code)

def translate_transaction_type(transaction_type):
	#Translates the transaction_type of a transaction - to its title. 
	#transactions statuses - deposit (1) , withdraw (2)
	status_dictionary = {1:'deposit', 2:'withdraw'}
	if(transaction_type in status_dictionary):
		return status_dictionary[transaction_type] + ("(%s)" % (transaction_type))
	else:
		return "wrong transaction type - " + str(transaction_type)


#Is_active function - relevant for some modules. 
def translate_active_state(is_active_state):
	#Translates the transaction_type of a transaction - to its title. 
	#transactions statuses - deposit (1) , withdraw (2)
	active_dictionary = {1:'active', 0:'unactive'}
	if(is_active_state in active_dictionary):
		return active_dictionary[is_active_state]
	else:
		return "wrong is_active state - optional values are unactive (0) and active (1) . "

