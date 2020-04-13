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
					<a href="/transactions/new/1">Open a new transaction - inside</a>
					<a href="/transactions/new/2">Open a new transaction - outside</a>
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
	#prints a form with transaction details, and allows to edit it. The form will refer to the edit function named transaction_edit()
	result = conn.select_query_single_row('''SELECT transaction_id, title, reason, status, 
													user_id_created, user_id_finished, user_id_last_status, 
													creation_date, transaction_date, 
													transaction_type, 
													supplier_id, costumer_id, 
													notes
											 FROM transactions 
											 WHERE transaction_id = '%s' ''' % (transaction_id) )

	#Print transaction edit form: 
	content = '''<form method="post" action="/transactions/update">
					<table>
						<tr><td>Transaction Id: </td><td><input type="hidden" name="transaction_id" value="''' + str(result[0]) + '''" />''' + str(result[0]) + '''</td></tr>
						<tr><td>Title: </td><td><input type="text" name="title" value="''' + str(result[1]) + '''" /></td></tr>
						<tr><td>Reason: </td><td><input type="text" name="reason" value="''' + str(result[2]) + '''" /></td></tr>
						<tr><td>Status: </td><td><input type="hidden" name="status" value="''' + str(result[3]) + '''" />''' + str(result[3]) + '''</td></tr>
						
						<tr><td>Created by: </td><td>''' + str(result[4]) + '''</td></tr>
						<tr><td>Closed by: </td><td>''' + str(result[5]) + '''</td></tr>
						<tr><td>Last user who changed status: </td><td>''' + str(result[6]) + '''</td></tr>
						
						<tr><td>Creation date: </td><td>''' + str(result[7]) + '''</td></tr>
						<tr><td>Transaction date: </td><td>''' + str(result[8]) + '''</td></tr>
						
						<tr><td>transaction type: </td><td><input type="text" name="transaction_type" value="''' + str(result[9]) + '''" /></td></tr>

						<tr><td>Supplier id: </td><td><input type="text" name="supplier_id" value="''' + str(result[10]) + '''" /></td></tr>
						<tr><td>Costumer id: </td><td><input type="text" name="costumer_id" value="''' + str(result[11]) + '''" /></td></tr>

						<tr><td>notes:</td><td><textarea name="notes">''' + str(result[12]) + '''</textarea></td></tr>
						<tr><td colspan="2"><input type="submit" value="Update Item" /></td></tr>
					</table>
				</form>
				<br />'''
	#Print actions list: 
	content += '''<form method="post" action="/transactions/update">
					<table>'''
	print("<tr></tr>")

	content +='''	</table>
				</form>
				<br />'''

	#Add actions list: 
	content += actions_list(transaction_id)


	#Return the created content
	return content

def transaction_update(transaction_id, title, reason, transaction_type, supplier_id, costumer_id, notes):
	#Adds a new warehouse to the warehuoses's list
	conn.execute_query("UPDATE transactions SET title = '%s' , reason = '%s' , transaction_type = '%s' , supplier_id = '%s' , costumer_id = '%s' , notes = '%s' , status = 2 WHERE transaction_id = '%s' AND user_id_last_status = %s " % (title, reason, transaction_type, supplier_id, costumer_id, notes, transaction_id, login.get_u_id()) )
	return 1

def transaction_view():
	pass




#These function will change transactions status - and change the storage. 
def transaction_delete(transaction_id):
	#Actually is just take an open transaction and changes its status to deleted (5) . 
	transaction_cancel(transaction_id)
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



# actions - 
# 	action_id
# 	item_id
# 	user_id
# 	transaction_id
# 	amount
# 	amount_before
# 	amount_after
# 	warehouse_id - NOT TO ADD! 
# 	storage_id - TO ADD IN FUTURE... 
# 	notes

#Actions functions - which will add, edit and delete actions from transactions. 
def actions_list(transaction_id):
	results = conn.select_query("SELECT action_id, item_id, amount, user_id, notes FROM actions WHERE transaction_id = %s" % (transaction_id))
	content = ""
	#Print the table only if actions have been added: 			
	if(len(results)==0): 
		content += "no item have been added yet - so no actions can be done! Add items to the transaction in the form below: " 
	else:
		content += '''<table>
						<tr><th>action id</th><th>item id</th><th>amount</th><th>added by</th><th>notes</th><th>actions: </th></tr>'''
		for result in results: 
			content +=	 "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><a href=\"/actions/remove/%s\">delete</a> | <a href=\"/actions/edit/%s\">edit</a></td></tr>" % (result[0], result[1], result[2], result[3], result[4], result[0], result[0])
		content += '''</table>
						total lines - ''' + str(len(results))
	
	#Add a form to add another action: 
	content += actions_add_form(transaction_id)

	return content

def actions_add_form(transaction_id): 
	results = conn.select_query("SELECT item_id, item_name, amount, m_unit FROM items")
	
	#In order to be able to add an action - at least one item has to be added to the database	
	if(len(results)==0): 
		return "no item have been added yet - so no actions can be done! <br />Go to the main page and choose items menu to add a new item" 

	content = '''
				<h3>Add another item: </h3>
				<form method="post" action="/actions/add">
					<input type="hidden" name="transaction_id" value="%s" />
					<table>
						<tr><td>item: </td><td><select name="item_id">''' % (transaction_id)
	for result in results:
		content += 	'''<option value="%s">%s - available %s %s</option>''' % (result[0], result[1], result[2], result[3])
	content += '''		</select></td></tr>
						<tr><td>amount: </td><td><input type="text" name="amount" /></td></tr>
						<tr><td>notes: </td><td><input type="text" name="notes" /></td></tr>
						<tr><td colspan="2"><input type="submit" value="add" /></td></tr>
					</table>
				</form>
				<br />'''

	return content

def add_action(transaction_id, item_id, amount, notes):
	user_id = login.get_u_id()
	new_action_id = conn.insert_query("actions", ['item_id', 'user_id', 'transaction_id', 'amount', 'notes'], 
		[item_id, user_id, transaction_id, amount, notes])
	return new_action_id

def remove_action(action_id):
	conn.execute_query("DELETE FROM actions WHERE action_id = %s" % (action_id))
	return 1

def edit_action_form(action_id):
	result = conn.select_query_single_row("SELECT action_id, transaction_id, item_id, amount, notes FROM actions WHERE action_id = %s" % (action_id))

	content = '''
				<h3>Edit action %s: </h3>
				<form method="post" action="/actions/edit">
					<table>
						<tr><td>action id: </td><td><input type="hidden" name="action_id" value="%s" />%s</td></tr>
						<tr><td>transaction id: </td><td><input type="hidden" name="transaction_id" value="%s" />%s</td></tr>
						<tr><td>item: </td><td><select name="item_id">''' % (result[0], result[0], result[0], result[1], result[1])

	items_list = conn.select_query("SELECT item_id, item_name, amount, m_unit FROM items")
	for item in items_list:
		if (item[0] == result[2]): #If it is the selected item, then attach "selected" attribute to it. 
			content += '''<option value="%s" selected>%s - available %s %s</option>''' % (item[0], item[1], item[2], item[3])
		else:
			content += '''<option value="%s">%s - available %s %s</option>''' % (item[0], item[1], item[2], item[3])
	
	content += 		'''</select></td></tr>
						<tr><td>amount: </td><td><input type="text" name="amount" value="%s" /></td></tr>
						<tr><td>notes: </td><td><input type="text" name="notes" value="%s" /></td></tr>
						<tr><td colspan="2"><input type="submit" value="add" /></td></tr>
					</table>
				</form>
				<br />''' % (result[3], result[4])
	return content

def edit_action(action_id, item_id, amount, notes):
	conn.execute_query("UPDATE actions SET item_id = '%s', amount = '%s' , notes = '%s', user_id = '%s' WHERE action_id = %s" %(item_id, amount, notes, str(login.get_u_id()) , action_id))
	return 1


