#!/bin/python
from datetime import date
import db_conn
import translate


conn = db_conn.db_conn() #Set the connection to the database, this will be used by the following functions. 

def storage_report():
	#Prints a report with all storage, including amounts and warehouse: 
	items = conn.select_query("SELECT item_id, item_name, m_unit, amount, warehouse_id FROM items")

	content =   '''<table>
						<tr><th>Item ID</th><th>Item name</th><th>Amount</th><th>Warehouse / Location</th></tr>'''

	for item in items:
		content += '''<tr><td>%s</td><td>%s</td><td>%s %s</td><td>%s</td></tr>''' % (item[0], item[1], item[3], item[2], translate.get_warehouse_name(item[4]))

	content += '''</table>
					Total items on list: ''' + str(len(items)) + ''' 
					<br />Report generated at: ''' + str(date.today().strftime("%d/%m/%Y"))

	return content

