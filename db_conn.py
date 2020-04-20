#!/usr/bin/python

import sqlite3 #import sqlite connection module fro python
# You already imported `sqlite3`, you could do : sqlite3.Error
from sqlite3 import Error #import the error module, used in the create_conn function

import logging #For the abillity to add logs in the terminal

# In Python classes are CamerCase: db_conn => DBConn(object)
class db_conn: 
	# It's better if you insert this in the constructor (__init__ method), and define it as : self.conn = ..
	conn = sqlite3.connect(r'./test.db', check_same_thread=False)

	def open_conn(self):
		#Connects to the database, if fails then abort the software. 
		try:
			self.conn = sqlite3.connect('test.db', check_same_thread=False)
		except Error as e:
			logging.error("connection to the sqlite failed! ")
			# Why print it? You could add it to the log message ^
			print(e)
			# You could raise an exception: `raise`, instead of ending the whole program
			sys.exit("connection to sqlite failed! ") 
		else: 
			logging.info("connection succeded")

	def close_con():
		#Closes the database. 
		conn.close

	def insert_query(self, tbl_name, param, values):
		#Accepts aprameters for insert query, return the id of the added row. 
		if len(param) != len(values) :
			# Raise an error (exception)
			exit('Error - params != values')

		param = str(param)[1:-1] # Nice!
		values = str(values)[1:-1]
		# If you're using Python3 try to stick with the new formatting: f"text here {variable here}" or str.format(..)
		query = ' INSERT INTO %s (%s) VALUES (%s) ' % (tbl_name,param,values)
		# It's better to use logging
		print(query)
		cur = self.conn.cursor()
		cur.execute(query)
		self.commit()
		return cur.lastrowid

	def execute_query(self, query): 
		#Execute a query and COMMITS IT! 
		cur = self.conn.cursor()
		cur.execute(query)
		self.commit()

	def execute_query_no_commit(self, query): 
		#Execute a query and NOT commiting it! 
		#This is useful for a series of transaction. Just don't forget to use commit() function in the end! 
		cur = self.conn.cursor()
		cur.execute(query)

	def select_query(self, query):
		# This code is repeated in a lot of places, try to use this method instead, e.g., in `select_query_single_row`
		#select query, returns a 2-dimensional array ("list" in python) with the results. 
		cur = self.conn.cursor() 
		cur.execute(query)
		return cur.fetchall()

	def select_query_single_row(self, query): 
		#select query, which return a one row results. A query with more then one result or zero - will prompt an error
		#The result is returned as a list. 
		cur = self.conn.cursor()
		cur.execute(query)
		results = cur.fetchall()
		
		#Check that only one result exists
		if(len(results) != 1): 
			logging.error("error - the result of the query is no one result. The num of results is - %s" % (str(len(results))))
			return False
		return results[0]

	def commit(self):
		#Sends a commit query to the database. Use this ONLY after finished the queries set. 
		#If the results won't be commited - then the changes won't be saved in the database! 
		query = ' commit; ' 
		cur = self.conn.cursor()
		cur.execute(query)



# #Example codes for testing
# db = db_conn()
# #build_db()
# db.open_conn()
# str = db.insert_query("warehouses",['wh_name','is_active'], ['main','1'])
# print(str)
# db.commit()

# db.execute_query("DELETE FROM warehouses")
# db.commit()
# print(db.select_query("select * from warehouses"))



