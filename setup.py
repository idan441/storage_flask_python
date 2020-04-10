#!/usr/bin/python

#The script creates the tables in the database: 
import db_conn

conn = db_conn.db_conn()

conn.execute_query('''CREATE TABLE warehouses 
				(wh_id		INTEGER		PRIMARY KEY,
				wh_name	TEXT	NOT NULL,
				is_active	INT		NOT NULL)
				''')
print("Table 'warehouses' created successfully")



conn.execute_query('''CREATE TABLE users 
				(u_id		INTEGER		PRIMARY KEY,
				u_name	TEXT	NOT NULL,
				is_active	INT		NOT NULL)
				''')
print("Table 'items' created successfully")



conn.execute_query('''CREATE TABLE items 
				(item_id		INTEGER		PRIMARY KEY,
				item_name	TEXT	NOT NULL,
				price	INT		NOT NULL
				amount	INT		NOT NULL
				warehouse_id	INT		NOT NULL)
				''')
print("Table 'items' created successfully")

