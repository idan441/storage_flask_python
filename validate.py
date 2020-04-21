#!/bin/python

import db_conn #DB connection module, allows accessing to the SQLite database. 
import re #RegEx module, which allows using RegEx. 
import logging

##############################################################
### This module includes functions which will be           ###
### used to validate input through forms and main.py file. ###
##############################################################



def sql_escape(input_string):
	input_string = input_string.replace("'", "''") #Escape the single quote - by doubling it. This is to avoid SQL injection. 
	return input_string


def is_number(input_string):
	print(input_string)
	if(re.search("^[0-9]+$", str(input_string))):
		return str(input_string)
	else:#In case the RegEx is false... exit from this script. (Unfortunately, due to late work on this part of the application, I chose to use exit() in case wrong values are sent - and not to use other good practice at this moment. ) 
		exit()
		#return False

def is_boolean(input_string):
	#Checks for boolean values of 0 or 1 in the accepted string. 
	#This is used to validate is_active values - which are 0 or 1 digits only! This is used in many modules such as users and trader! 
	if(input_string in ["0", "1"]): 
		return input_string
	else:
		logging.warning("is_boolean - USING OF ROBIDDEN VALUE!! Optional values - 0 or 1 ! INSERTED STRING - " + str(input_string))
		exit("wrong value with wrong characters. See logging for more information. ")


#These functions will accept id number of items, warehuoses, transactione etc... and will check if they really are exist. 
conn = db_conn.db_conn() #Set the connection to the database, this will be used by the following functions. 

def is_wh(input_string): 
	#Checks if the string contains an existing warehuose(wh) ID, which exists in the datbase. 
	if(conn.select_query_single_row("SELECT wh_id FROM warehouses WHERE wh_id=%s" % (is_number(input_string)))):
		return input_string
	else:
		logging.warning("is_wh - wrong value! INSERTED STRING - " + str(input_string))
		exit("wrong value with wrong characters. See logging for more information. ")

def is_user(input_string): 
	#Checks if the string contains an existing user ID, which exists in the datbase. 
	if(conn.select_query_single_row("SELECT u_id FROM users WHERE u_id=%s" % (is_number(input_string)))):
		return input_string
	else:
		logging.warning("is_user - wrong value! INSERTED STRING - " + str(input_string))
		exit("wrong value with wrong characters. See logging for more information. ")

def is_item(input_string): 
	#Checks if the string contains an existing item ID, which exists in the datbase. 
	if(conn.select_query_single_row("SELECT item_id FROM items WHERE item_id=%s" % (is_number(input_string)))):
		return input_string
	else:
		logging.warning("is_item - wrong value! INSERTED STRING - " + str(input_string))
		exit("wrong value with wrong characters. See logging for more information. ")

def is_trader(input_string): 
	#Checks if the string contains an existing trader ID, which exists in the datbase. 
	print(input_string)
	if(conn.select_query_single_row("SELECT t_id FROM traders WHERE t_id=%s" % (is_number(input_string)))):
		return input_string
	else:
		logging.warning("is_trader - wrong value! INSERTED STRING - " + str(input_string))
		exit("wrong value with wrong characters. See logging for more information. ")

def is_transaction(input_string): 
	#Checks if the string contains an transaction ID, which exists in the datbase. 
	if(conn.select_query_single_row("SELECT transaction_id FROM transactions WHERE transaction_id=%s" % (is_number(input_string)))):
		return input_string
	else:
		logging.warning("is_transaction - wrong value! INSERTED STRING - " + str(input_string))
		exit("wrong value with wrong characters. See logging for more information. ")

def is_action(input_string): 
	#Checks if the string contains an existing action ID, which exists in the datbase. 
	if(conn.select_query_single_row("SELECT action_id FROM actions WHERE action_id=%s" % (is_number(input_string)))):
		return input_string
	else:
		logging.warning("is_action - wrong value! INSERTED STRING - " + str(input_string))
		exit("wrong value with wrong characters. See logging for more information. ")


