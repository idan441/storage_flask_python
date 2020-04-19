#!/bin/python
import db_conn
import translate

conn = db_conn.db_conn() #Set the connection to the database, this will be used by the following functions. 

def items_list(): 
	results = conn.select_query("SELECT item_id, item_name, amount, price, warehouse_id, m_unit FROM items")
	content = ""
	
	if(len(results)==0): 
		content += "no items have been created yet! " 
	else: 
		content = "<table><th>Id</th><th>name</th><th>amount</th><th>meas. u.</th><th>price</th><th>warehouse</th><th>actions</td>"
		for result in results: 
			content += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><a href=\"/items/edit/%s\">edit</a></td></tr>" % ( result[0], result[1], result[2], result[5], result[3], translate.get_warehouse_name(result[4]), result[0] )
		content += "</table>" 
		content += "count: " + str(len(results))
	
	content += '''<br /><br />
					<div class="button"><a href="/items/add">Add a new item</a></div>
				<br /><br />
				<a href="/reports/storage">storage report</a>'''
	return content

def item_add_form(): 
	#returns HTML code for a form for adding a new item
	content =	'''<form method="post" action="/items/add">
						<table>
							<tr><td>Item name: </td><td><input type="text" name="item_name" /></td></tr>
							<tr><td>Amount: </td><td><input type="text" name="amount" /></td></tr>
							<tr><td>Measurement unit: </td><td><input type="text" name="m_unit" /></td></tr>
							<tr><td>Price: </td><td><input type="text" name="price" /></td></tr>
							<tr><td>Warehouse / Location: </td><td>
								<select name="warehouse_id">'''

	#Add ACTIVE warehouses select list: 
	warehouses_list = conn.select_query("SELECT wh_id, wh_name FROM warehouses WHERE is_active = 1")
	if(len(warehouses_list) == 0):
		return "No warehouses are available. You need to have at least 1 active warehouse to relate the item to. Activate or add a new warehouse! " 
	else:
		for wh in warehouses_list:
			content += 			'''<option value="%s">%s</option>''' %(wh[0], wh[1])

	content +=	'''				</select>
							</td></tr>
							<tr><td>Supplier: </td><td>
								<select name="supplier_id">'''
	#Add ACTIVE warehouses select list: 
	suppliers_list = conn.select_query("SELECT t_id, t_name FROM traders WHERE is_supplier = 1 AND is_active = 1")
	if(len(suppliers_list) == 0):
		return "No suppliers available. You need to have at least 1 active supplier to relate the item to. Active an existing supplier or create a new supplier through the <a href=""/traders"">traders list. </a>"
	for sp in suppliers_list:
			content += 			'''<option value="%s">%s</option>''' %(sp[0], sp[1])

	content +=					'''</select>
							</td></tr>
							<tr><td>notes:</td><td><textarea name="notes"></textarea></td></tr>
							<tr><td colspan="2"><input type="submit" value="add new item" /></td></tr>
						</table>
					</form>
				'''
	return content

def item_add(item_name, amount, m_unit, price, supplier_id, warehouse_id, notes):
	new_item_id = conn.insert_query("items", ['item_name','amount','m_unit','price','supplier_id','warehouse_id','notes'], [item_name, amount, m_unit, price, supplier_id, warehouse_id, notes])
	return new_item_id

def item_edit(item_id):
	#Adds a new warehouse to the warehuoses's list
	result = conn.select_query_single_row("SELECT item_id, item_name, amount, m_unit, price, supplier_id, warehouse_id, notes FROM items WHERE item_id = '%s' " % (item_id) )

	content = '''<form method="post" action="/items/edit">
					<table>
						<tr><td>Item Id: </td><td><input type="hidden" name="item_id" value="''' + str(result[0]) + '''" />''' + str(result[0]) + '''</td></tr>
						<tr><td>Item name: </td><td><input type="text" name="item_name" value="''' + str(result[1]) + '''" /></td></tr>
						<tr><td>Amount: </td><td><input type="text" name="amount" value="''' + str(result[2]) + '''" /></td></tr>
						<tr><td>Measurement unit: </td><td><input type="text" name="m_unit" value="''' + str(result[3]) + '''" /></td></tr>
						<tr><td>Price: </td><td><input type="text" name="price" value="''' + str(result[4]) + '''" /></td></tr>
						<tr><td>Warehouse / Location: </td>
						<td>
							<select name="warehouse_id">'''

	#Add ACTIVE warehouses select list: 
	warehouses_list = conn.select_query("SELECT wh_id, wh_name FROM warehouses WHERE is_active = 1 OR wh_id = %s" % (result[5]))
	if(len(warehouses_list) == 0):
		return "No warehouses are available. You need to have at least 1 active warehouse to relate the item to. <a href=""/warehouse"">Activate or add a new warehouse! </a>" 
	else:
		for wh in warehouses_list:
			if(wh[0] == result[6]):
				content += 			'''<option value="%s" selected>%s</option>''' %(wh[0], wh[1])
			else:
				content += 			'''<option value="%s">%s</option>''' %(wh[0], wh[1])

	content +=		'''		</select>
						</td></tr>
						<tr><td>supplier: </td><td>
							<select name="supplier_id">'''

	#Add ACTIVE suppliers select list: 
	suppliers_list = conn.select_query("SELECT t_id, t_name FROM traders WHERE (is_supplier = 1 AND is_active = 1) OR t_id = %s" % (result[6]))
	for sp in suppliers_list:
		if(sp[0] == result[5]):
			content += 			'''<option value="%s" selected>%s</option>''' %(sp[0], sp[1])
		else:
			content += 			'''<option value="%s">%s</option>''' %(sp[0], sp[1])

	content +=		'''		</select>
						</td></tr>
						<tr><td>notes:</td><td><textarea name="notes">''' + str(result[7]) + '''</textarea></td></tr>
						<tr><td colspan="2"><input type="submit" value="Update Item" /></td></tr>
					</table>
				</form>
				<br />'''

	#Print warnings - if the warehuose or supplier assigned to this item are inactive. 
	if(translate.is_trader_supplier(result[6]) == 0):
		content += "<p style=""color:red;"">The supplier assigned to this item is not active! It is recommended to change the supplier or re-creating the item with its new supplier. </p>"
	if(translate.is_warehouse_active(result[5]) == 0):
		content += "<p style=""color:red;"">The warehouse assigned to this item is not active! It is recommended to change the warehouse to the current warehouse where the item located at. </p>"	


	content += '''
				<h3>Reports: </h3>
				<a href="/reports/transactions_by_item?i_id=''' + item_id + '''">Transactions done by this trade</a>
				<br />
				<p>
					<b>Important - changing item's amount through this form: </b><br />
					Though you can change the amount of the item in this form, it is recommended to change it using transactions. By using transactions you can document where and who changed the amount. Changing the amount here will be permanent without being able to know when or why the change was done! 
				</p>'''

	return content

def item_update(item_id, item_name, amount, m_unit, price, supplier_id, warehouse_id, notes):
	#Adds a new warehouse to the warehuoses's list
	conn.execute_query("UPDATE items SET item_name = '%s' , amount = '%s' , m_unit = '%s' , price = '%s' , supplier_id = '%s' , warehouse_id = '%s' , notes = '%s' WHERE item_id = '%s' " % (item_name, amount, m_unit, price, supplier_id, warehouse_id, notes, item_id))
	return 1


