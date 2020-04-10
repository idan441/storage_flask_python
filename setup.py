#!/usr/bin/python

#The script creates the tables in the database: 
import db_conn

conn = db_conn.db_conn()

conn.execute_query_transaction('''CREATE TABLE warehouses 
				(wh_id		INTEGER		PRIMARY KEY,
				wh_name	TEXT	NOT NULL,
				is_active	INT		NOT NULL)
				''')
print("Table 'warehouses' created successfully")



conn.execute_query_transaction('''CREATE TABLE users 
				(u_id		INTEGER		PRIMARY KEY,
				u_name	TEXT	NOT NULL, 
				password	TEXT	NOT NULL,
				is_active	INT		NOT NULL,
				is_admin	INT		NOT NULL)
				''')
print("Table 'users' created successfully")



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
print("Table 'items' created successfully")



conn.execute_query_transaction('''CREATE TABLE transactions 
				(transaction_id		INTEGER		PRIMARY KEY,
				title	TEXT	NOT NULL,
				user_id	INT		NOT NULL, 
				reason	TEXT	NOT NULL,
				creation_date_date	INT		NOT NULL, 
				transaction_date	INT		NOT NULL, 
				status	INT		NOT NULL, 
				notes	TEXT, 
				transaction_type	INT		NOT NULL, 
				supplier_id	INT		NOT NULL, 
				costumer_id	INT		NOT NULL)
				''')
print("Table 'transaction' created successfully")



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
print("Table 'transaction' created successfully")


