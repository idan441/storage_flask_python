#!/usr/bin/python

#The script creates the tables in the database: 
import db_conn


print("Connecting to the database: ")
print ("Creating the database")  
conn = db_conn.db_conn()



print("Creating database tables - ")
conn.execute_query_transaction('''CREATE TABLE warehouses 
				(wh_id		INTEGER		PRIMARY KEY,
				wh_name	TEXT	NOT NULL,
				is_active	INT		NOT NULL)
				''')
print("\tTable 'warehouses' created successfully")



conn.execute_query_transaction('''CREATE TABLE users 
				(u_id		INTEGER		PRIMARY KEY,
				d_name	TEXT	NOT NULL, 
				u_name	TEXT	NOT NULL, 
				password	TEXT	NOT NULL,
				is_active	INT		NOT NULL,
				is_admin	INT		NOT NULL)
				''')
print("\tTable 'users' created successfully")



conn.execute_query_transaction('''CREATE TABLE items 
				(item_id		INTEGER		PRIMARY KEY,
				item_name	TEXT	NOT NULL,
				amount	INT		NOT NULL, 
				m_unit	TEXT	NOT NULL,
				price	INT		NOT NULL, 
				supplier_id	INT		NOT NULL, 
				warehouse_id	INT		NOT NULL, 
				notes	TEXT)
				''')
print("\tTable 'items' created successfully")



conn.execute_query_transaction('''CREATE TABLE transactions 
				(transaction_id		INTEGER		PRIMARY KEY,
				title	TEXT,
				user_id_created	INT		NOT NULL,
				user_id_finished	INT,
				user_id_last_status	INT		NOT NULL, 
				reason	TEXT,
				creation_date	TEXT		NOT NULL, 
				transaction_date	TEXT, 
				status	INT		NOT NULL, 
				notes	TEXT, 
				transaction_type	INT		NOT NULL, 
				supplier_id	INT, 
				costumer_id	INT)
				''')
print("\tTable 'transactions' created successfully")



conn.execute_query_transaction('''CREATE TABLE actions 
				(actions_id		INTEGER		PRIMARY KEY,
				item_id	INT		NOT NULL, 
				user_id	INT		NOT NULL, 
				transaction_id	INT		NOT NULL, 
				amount_added	INT		NOT NULL, 
				amount_subbed	INT		NOT NULL, 
				amound_before	INT		NOT NULL, 
				amount_after	INT		NOT NULL, 
				notes	TEXT)
				''')
print("\tTable 'actions' created successfully")



print("*** Finished creating the database tables *** \n\n")

print("Creating admin user - ")
print("\tThis user will be used for the first access - remember its details!") 
print ("\tUse letters and numbers only") 
print("\t Enter username: ")
input_username = input()
print("\t ENter password: ")
input_password = input()

####Put here the query to create the admin user! make sure to set the is_admin = 1 ! 

print("*** Finished adding the admin user *** \n\n") 


