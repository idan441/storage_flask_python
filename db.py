#!/usr/bin/python

import sqlite3 #import sqlite connection module fro python
from sqlite3 import Error #import the error module, used in the create_conn function

import logging #For the abillity to add logs in the terminal


class dbcon: 

	conn = sqlite3.connect(r'./test.db')

	def open_conn(self):
		#Connects to the database, if fails then abort the software. 
		try:
			self.conn = sqlite3.connect('test.db')
		except Error as e:
			logging.error("connection to the sqlite failed! ")
			print(e)
			sys.exit("connection to sqlite failed! ") 
		else: 
			logging.info("connection succeded")

	def close_con():
		#Closes the database. 
		conn.close

	def insert_query(self, tbl_name, param, values):
		#Accepts aprameters for insert query, return the id of the added row. 
		if len(param) != len(values) :
			exit('Error - params != values')

		param = str(param)[1:-1]
		values = str(values)[1:-1]
		
		query = ' INSERT INTO %s (%s) VALUES (%s) ' % (tbl_name,param,values)
		print(query)
		cur = self.conn.cursor()
		cur.execute(query)
		return cur.lastrowid


	def update_query_no_where(self, tbl_name, param, values): 
		return update_query(tbl_name, param, values, [], [])
	def update_query(self, tbl_name, param, values, where_param, where_value): 
		if len(param) != len(values) :
			exit('Error - params != values')
		if len(where_param) != len(where_values) :
			exit('Error - where_params != where_values')
		
		
		query = ' UPDATE %s SET ' % (tbl_name)
		
		#Add the updated parameters - 
		for i in range(len(param)) : 
			query += ' %s = \'%s\'' % (param[i], values[i])
			if (i != len(param)-1) : 
				query += ', '
	
		#Add the where clause, if where_param and where_value are set) 
		if(where_param != 0):
			query += " WHERE " 
			for i in range(len(param)) : 
				query += ' %s = \'%s\'' % (param[i], values[i])
				if (i != len(param)-1) : 
					query += ', '
				print(i)

		print(query)
		cur = self.conn.cursor()
		cur.execute(query)

	def select_query(self, query): 
		#select query, returns a 2-dimensional array ("list" in python) with the results. 
		cur = self.conn.cursor() 
		cur.execute(query)
		return cur.fetchall()

	def commit(self):
		#Sends a commit query to the database. Use this ONLY after finished the queries set. 
		#If the results won't be commited - then the changes won't be saved in the database! 
		query = ' commit; ' 
		cur = self.conn.cursor()
		cur.execute(query)

	def rollback(self): 
		#Cancel the previous queries before the latest commit. (or from the start of the code. ) 
		#The opposite of commit. 
		query = ' rollback; ' 
		cur = self.conn.cursor()
		cur.execute(query)


#Create tables: 
def build_db():
	db.conn.execute('''CREATE TABLE warehouses 
					(wh_id		INTEGER		PRIMARY KEY,
					wh_name	TEXT	NOT NULL,
					is_active	INT		NOT NULL)
					''')
	print("Table 'warehouses' created successfully")




db = dbcon()
#build_db()
db.open_conn()
str = db.insert_query("warehouses",['wh_name','is_active'], ['main','1'])
print(str)
db.commit()

db.update_query("warehouses", ["wh_name"], ["mainnn"])

print(db.select_query("select * from warehouses"))



