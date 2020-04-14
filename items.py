#!/bin/python
import db_conn

conn = db_conn.db_conn() #Set the connection to the database, this will be used by the following functions. 

def items_list(): 
	results = conn.select_query("SELECT item_id, item_name, amount, price, warehouse_id FROM items")
	content = ""
	
	if(len(results)==0): 
		content += "no items have been created yet! " 
	else: 
		content = "<table><th>Id</th><th>name</th><th>amount</th><th>price</th><th>warehouse</th><th>actions</td>"
		for result in results: 
			content += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><a href=\"/items/edit/%s\">edit</a></td></tr>" % ( result[0], result[1], result[2], result[3], result[4], result[0] )
		content += "</table>" 
		content += "count: " + str(len(results))
	
	content += '''<br />
					<a href="/items/add">Add a new item</a>
				<br />'''
	return content

def item_add_form(): 
	#returns HTML code for a form for adding a new item
	content =	'''<form method="post" action="/items/add">
						<table>
							<tr><td>Item name: </td><td><input type="text" name="item_name" /></td></tr>
							<tr><td>Amount: </td><td><input type="text" name="amount" /></td></tr>
							<tr><td>Measurement unit: </td><td><input type="text" name="m_unit" /></td></tr>
							<tr><td>Price: </td><td><input type="text" name="price" /></td></tr>
							<tr><td>Warehouse / Location: </td><td><input type="text" name="warehouse_id" /></td></tr>
							<tr><td>Supplier: </td><td><input type="text" name="supplier_id" /></td></tr>
							<tr><td>notes:</td><td><textarea name="notes"></textarea></td></tr>
							<tr><td colspan="2"><input type="submit" value="add new item" /></td></tr>
						</table>
					</form>
				'''
	return content

def item_add(item_name, amount, m_unit, price, supplier_id, warehouse_id, notes):
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


