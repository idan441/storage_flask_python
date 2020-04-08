#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('test.db')

print("Opened database successfully, if the database wasn't exist - then it was created")


conn.execute('''CREATE TABLE warehouses
		         (wh_id         INT     PRIMARY KEY     NOT NULL,
		         name           TEXT    NOT NULL,
		         is_active      INT     NOT NULL)
				''')
print("Table 'warehouse' created successfully")


