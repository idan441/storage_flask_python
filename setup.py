#!/usr/bin/python

#The script creates the tables in the database: 
import db_conn


print("Connecting to the database: ")
print ("Creating the database")  
conn = db_conn.db_conn()



print("Creating database tables - ")
conn.execute_query_no_commit('''CREATE TABLE warehouses 
				(wh_id		INTEGER		PRIMARY KEY,
				wh_name	TEXT	NOT NULL,
				is_active	INT		NOT NULL DEFAULT 1)
				''')
print("\tTable 'warehouses' created successfully")



conn.execute_query_no_commit('''CREATE TABLE users 
				(u_id		INTEGER		PRIMARY KEY,
				d_name	TEXT	NOT NULL, 
				u_name	TEXT	NOT NULL, 
				password	TEXT	NOT NULL,
				is_active	INT		NOT NULL DEFAULT 1,
				is_admin	INT		NOT NULL DEFAULT 0)
				''')
print("\tTable 'users' created successfully")



conn.execute_query_no_commit('''CREATE TABLE items 
				(item_id		INTEGER		PRIMARY KEY,
				item_name	TEXT	NOT NULL,
				amount	INT		NOT NULL DEFAULT 0, 
				m_unit	TEXT	NOT NULL DEFAULT "Units",
				price	INT		NOT NULL DEFAULT 0, 
				supplier_id	INT		NOT NULL, 
				warehouse_id	INT		NOT NULL, 
				notes	TEXT DEFAULT "")
				''')
print("\tTable 'items' created successfully")



conn.execute_query_no_commit('''CREATE TABLE transactions 
				(transaction_id		INTEGER		PRIMARY KEY,
				title	TEXT DEFAULT "",
				user_id_created	INT		NOT NULL,
				user_id_finished	INT,
				user_id_last_status	INT		NOT NULL, 
				reason	TEXT DEFAULT "",
				creation_date	TEXT		NOT NULL, 
				transaction_date	TEXT DEFAULT "", 
				status	INT		NOT NULL DEFAULT 1, 
				notes	TEXT DEFAULT "", 
				transaction_type	INT		NOT NULL, 
				trader_id	INT)
				''')
print("\tTable 'transactions' created successfully")



conn.execute_query_no_commit('''CREATE TABLE actions 
				(action_id		INTEGER		PRIMARY KEY,
				item_id	INT		NOT NULL, 
				user_id	INT		NOT NULL, 
				transaction_id	INT		NOT NULL, 
				amount	INT		NOT NULL DEFAULT 0, 
				notes	TEXT DEFAULT "")
				''')
print("\tTable 'actions' created successfully")



conn.execute_query_no_commit('''CREATE TABLE traders 
				(t_id		INTEGER		PRIMARY KEY,
				t_name	INT		NOT NULL, 
				is_active	INT		NOT NULL, 
				address	INT default "", 
				contact_name	INT default"", 
				phone	TEXT default "", 
				is_supplier	INT		NOT NULL, 
				is_costumer	INT		NOT NULL, 
				notes	TEXT default ""
				)
				''')
print("\tTable 'traders' created successfully")


print("*** Finished creating the database tables *** \n\n")



print("Creating admin user - ")
print("\tThis user will be used for the first access - remember its details!") 
print ("\tUse letters and numbers only") 

print("Enter username: ")
input_username = input()
print("Enter Display: (First + last name, Which will be shown on forms and reports.")
input_name = input()
print("Enter password: ")
input_password = input()

import users
conn.execute_query("INSERT INTO users (u_name, password, is_active, is_admin, d_name) VALUES ('%s','%s', 1, 1, '%s')" % (input_username, input_password, input_name))
print("Finished creating admin username, please remember your passwrod and username in order to log in! ") 

print("*** Finished adding the admin user *** \n\n") 


print("*** Finished the installation. You can login to the application. ")