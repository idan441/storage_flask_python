#!/usr/bin/python

#The script creates the tables in the database: 
from db_conn import dbcon 


db.conn.execute('''CREATE TABLE warehouses 
				(wh_id		INTEGER		PRIMARY KEY,
				wh_name	TEXT	NOT NULL,
				is_active	INT		NOT NULL)
				''')
print("Table 'warehouses' created successfully")


db.conn.execute('''CREATE TABLE items 
				(item_id		INTEGER		PRIMARY KEY,
				item_name	TEXT	NOT NULL,
				price	INT		NOT NULL
				amount	INT		NOT NULL
				warehouse_id	INT		NOT NULL)
				''')
print("Table 'items' created successfully")

