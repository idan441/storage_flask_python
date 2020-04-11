#!/bin/python
from datetime import date
import login #User login functions - for accessing the session of the connected user
import db_conn

conn = db_conn.db_conn() #Set the connection to the database, this will be used by the following functions. 

def transactions_list(): 
	results = conn.select_query("SELECT transaction_id, title, creation_date, transaction_date, status FROM transactions")
	content = ""
	
	if(len(results)==0): 
		content += "no transactions have been created yet! " 
	else: 
		content = '''<table>
						<th>Id</th><th>Title</th><th>Creation date</th><th>transaction_date</th><th>status</th>
						<tr>'''
		for result in results: 
			if(result[4] == "5"): #status = 5 = transaction is finished and can only be viewed
				content += "<td><a href=\"/transactions/view/%s\">%s</a></td><td><a href=\"/transactions/view/%s\">%s</a></td>" % (result[0], result[0], result[0], result[1])
			else: 
				content += "<td><a href=\"/transactions/edit/%s\">%s</a></td><td><a href=\"/transactions/edit/%s\">%s</a></td>" % (result[0], result[0], result[0], result[1])
			content += "<td>%s</td><td>%s</td><td>%s</td></tr>" % ( result[2], result[3], result[4] )

		content += "</table>" 
		content += "count: " + str(len(results))
	
	content += '''<br />
					<a href="/transactions/open/1">Open a new transaction - inside</a>
					<a href="/transactions/open/2">Open a new transaction - outside</a>
				<br />
				<p>transactions statuses - created (1) , open (2) , finished (3) , canceled (4) , deleted (5) </p>
				'''
	return content

def transaction_new(transaction_type):
	#This function will open a new transaction, and will return the new transaction's id. 
	#This id will be used by the routing funciton in main.py to route the user to the edit page of the new transaction. 
	new_transaction_id = conn.insert_query("transactions", ['transaction_type', 'user_id_created', 'user_id_last_status', 'creation_date', 'status'], [transaction_type, login.get_u_id(), login.get_u_id(), date.today().strftime("%d/%m/%Y"), 1])
	return new_transaction_id

def transaction_edit(transaction_id):
	#Adds a new warehouse to the warehuoses's list
	result = conn.select_query_single_row("SELECT item_id, item_name, amount, m_unit, price, supplier_id, warehouse_id, notes FROM items WHERE item_id = '%s' " % (item_id) )

	return '''<form method="post" action="/transactions/edit">
					<table>
						<tr><td>Transaction Id: </td><td><input type="hidden" name="item_id" value="''' + str(result[0]) + '''" />''' + str(result[0]) + '''</td></tr>
						<tr><td>Title: </td><td><input type="text" name="item_name" value="''' + str(result[1]) + '''" /></td></tr>
						<tr><td>Reason: </td><td><input type="text" name="item_name" value="''' + str(result[1]) + '''" /></td></tr>
						<tr><td>Status: </td><td><input type="text" name="item_name" value="''' + str(result[1]) + '''" /></td></tr>
						
						<tr><td>Created by: </td><td><input type="text" name="amount" value="''' + str(result[2]) + '''" /></td></tr>
						<tr><td>Closed by: </td><td><input type="text" name="m_unit" value="''' + str(result[3]) + '''" /></td></tr>
						<tr><td>Last user who changed status: </td><td><input type="text" name="price" value="''' + str(result[4]) + '''" /></td></tr>
						
						<tr><td>Creation date: </td><td><input type="text" name="warehouse_id" value="''' + str(result[5]) + '''" /></td></tr>
						<tr><td>Transaction date: </td><td><input type="text" name="warehouse_id" value="''' + str(result[5]) + '''" /></td></tr>
						
						<tr><td>transaction type: </td><td><input type="text" name="warehouse_id" value="''' + str(result[5]) + '''" /></td></tr>

						<tr><td>Supplier id: </td><td><input type="text" name="warehouse_id" value="''' + str(result[5]) + '''" /></td></tr>
						<tr><td>Costumer id: </td><td><input type="text" name="supplier_id" value="''' + str(result[6]) + '''" /></td></tr>

						<tr><td>notes:</td><td><textarea name="notes">''' + str(result[7]) + '''</textarea></td></tr>
						<tr><td colspan="2"><input type="submit" value="Update Item" /></td></tr>
					</table>
				</form>
				<br />'''

def transaction_update(item_id, item_name, amount, m_unit, price, supplier_id, warehouse_id, notes):
	#Adds a new warehouse to the warehuoses's list
	conn.execute_query("UPDATE items SET item_name = '%s' , amount = '%s' , m_unit = '%s' , price = '%s' , supplier_id = '%s' , warehouse_id = '%s' , notes = '%s' WHERE item_id = '%s' " % (item_name, amount, m_unit, price, supplier_id, warehouse_id, notes, item_id))
	return "item %s(%s) updated!" % (item_name, item_id)

def transaction_view():
	pass




#These function will change transactions status - and change the storage. 
def transaction_delete(transaction_id):
	#Only transaction which hasn't been finished or canceled - can be deleted. 
	pass

def transaction_cancel(transaction_id):
	#Cancel transaction - only for finished transaction (3) . 
	pass

def transaction_close(transaction_id):
	#This function will close the transaction - and will change the items amount. 
	pass

def transaction_open(transaction_id):
	#Can open a closed transaction - while changing the storage - and will return the items. 
	pass





#Actions functions - which will add, edit and delete actions from transactions. 
def add_action():
	pass

def remove_action():
	pass

def edit_action():
	pass

