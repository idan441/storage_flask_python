#!/bin/python
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
					<a href="/transactions/open">Open a new transaction</a>
				<br />
				<p>transactions statuses - created (1) , open (2) , finished (3) , canceled (4) , deleted (5) </p>
				'''
	return content

def transaction_open_form(): 
	#returns HTML code for a form for adding a new transaction
	#Mandatory fields - title, used_id_created, creation_date, transaction_type, status
	content =	'''<form method="post" action="/transactions/open">
						<table>
							<tr><td>Title: </td><td><input type="text" name="title" /></td></tr>
							<tr><td>Transaction type: </td><td><input type="text" name="amount" /></td></tr>
							<tr><td colspan="2">Put the Id in the field according to the transaction type: (1 = inside = supplier) ( 2 = outside = costumer)
							<tr><td>Transaction type: </td><td><input type="text" name="amount" /></td></tr>
							<tr><td>Transaction type: </td><td><input type="text" name="amount" /></td></tr>
							<tr><td colspan="2"><input type="submit" value="open new transaction" /></td></tr>
						</table>
					</form>
					<br />
					<p> transaction types - (1) inside , (2) outside </p>
				'''
	return content


def transaction_open(item_name, amount, m_unit, price, supplier_id, warehouse_id, notes):
	new_item_id = conn.insert_query("items", ['item_name','amount','m_unit','price','supplier_id','warehouse_id','notes'], [item_name, amount, m_unit, price, supplier_id, warehouse_id, notes])
	return " new user added! with new id - " + str(new_item_id)

def item_edit(item_id):
	#Adds a new warehouse to the warehuoses's list
	result = conn.select_query_single_row("SELECT item_id, item_name, amount, m_unit, price, supplier_id, warehouse_id, notes FROM items WHERE item_id = '%s' " % (item_id) )

	return '''<form method="post" action="/items/edit">
					<table>
						<tr><td>Item Id: </td><td><input type="hidden" name="item_id" value="''' + str(result[0]) + '''" />''' + str(result[0]) + '''</td></tr>
						<tr><td>Item name: </td><td><input type="text" name="item_name" value="''' + str(result[1]) + '''" /></td></tr>
						<tr><td>Amount: </td><td><input type="text" name="amount" value="''' + str(result[2]) + '''" /></td></tr>
						<tr><td>Measurement unit: </td><td><input type="text" name="m_unit" value="''' + str(result[3]) + '''" /></td></tr>
						<tr><td>Price: </td><td><input type="text" name="price" value="''' + str(result[4]) + '''" /></td></tr>
						<tr><td>Warehouse / Location: </td><td><input type="text" name="warehouse_id" value="''' + str(result[5]) + '''" /></td></tr>
						<tr><td>supplier: </td><td><input type="text" name="supplier_id" value="''' + str(result[6]) + '''" /></td></tr>
						<tr><td>notes:</td><td><textarea name="notes">''' + str(result[7]) + '''</textarea></td></tr>
						<tr><td colspan="2"><input type="submit" value="Update Item" /></td></tr>
					</table>
				</form>
				<br />'''

def item_update(item_id, item_name, amount, m_unit, price, supplier_id, warehouse_id, notes):
	#Adds a new warehouse to the warehuoses's list
	conn.execute_query("UPDATE items SET item_name = '%s' , amount = '%s' , m_unit = '%s' , price = '%s' , supplier_id = '%s' , warehouse_id = '%s' , notes = '%s' WHERE item_id = '%s' " % (item_name, amount, m_unit, price, supplier_id, warehouse_id, notes, item_id))
	return "item %s(%s) updated!" % (item_name, item_id)


