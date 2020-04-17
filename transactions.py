#!/bin/python
from datetime import date
import login #User login functions - for accessing the session of the connected user
import db_conn
import translate

conn = db_conn.db_conn() #Set the connection to the database, this will be used by the following functions. 

def transactions_list(): 
	results = conn.select_query("SELECT transaction_id, title, creation_date, transaction_date, status, transaction_type FROM transactions ORDER BY creation_date DESC, status")
	content = ""
	
	if(len(results)==0): 
		content += "no transactions have been created yet! " 
	else: 
		content = '''<table>
						<th>Id</th><th>Title</th><th>Type</th><th>Creation date</th><th>Transaction date</th><th>status</th>
						<tr>'''
		for result in results: 
			if(result[4] == "5"): #status = 5 = transaction is finished and can only be viewed
				content += "<td><a href=\"/transactions/view/%s\">%s</a></td><td><a href=\"/transactions/view/%s\">%s</a></td>" % (result[0], result[0], result[0], result[1])
			else: 
				content += "<td><a href=\"/transactions/edit/%s\">%s</a></td><td><a href=\"/transactions/edit/%s\">%s</a></td>" % (result[0], result[0], result[0], result[1])
			content += "<td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % ( translate.translate_transaction_type(result[5]) ,result[2], result[3], translate.translate_status(result[4]) )

		content += "</table>" 
		content += "count: " + str(len(results))
	
	content += '''<br /><br />
					<h3>Add a new transaction: </h3>
					<div class="button"><a href="/transactions/new/1">Open a new transaction - deposit</a></div>
					<div class="button"><a href="/transactions/new/2">Open a new transaction - withdraw</a></div>
				<br /><br /><br />

				<h4>Key lists: </h4>
				<p><b>transactions statuses - </b>created (1) , open (2) , finished (3) , canceled (4) , deleted (5) </p>
				<p><b>transactions types - </b>deposit (1) , withdraw (2) </p>
				<p>Need more help about understanding what the meanings of transactions? See the <a href="/help">help page</a></p>
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
													trader_id,
													notes
											 FROM transactions 
											 WHERE transaction_id = '%s' ''' % (transaction_id) )

	#Print transaction edit form: 
	content = '''<form method="post" action="/transactions/update">
					<table>
						<tr><td>Transaction Id: </td><td><input type="hidden" name="transaction_id" value="''' + str(result[0]) + '''" />''' + str(result[0]) + '''</td></tr>
						<tr><td>Title: </td><td><input type="text" name="title" value="''' + str(result[1]) + '''" /></td></tr>
						<tr><td>Reason: </td><td><input type="text" name="reason" value="''' + str(result[2]) + '''" /></td></tr>
						<tr><td>Status: </td><td><input type="hidden" name="status" value="''' + str(result[3]) + '''" />''' + translate.translate_status(result[3]) + '''</td></tr>
						
						<tr><td>Created by: </td><td>''' + translate.get_user_d_name(result[4]) + '''</td></tr>
						<tr><td>Closed by: </td><td>''' + translate.get_user_d_name(result[5]) + '''</td></tr>
						<tr><td>Last user who changed status: </td><td>''' + translate.get_user_d_name(result[6]) + '''</td></tr>
						
						<tr><td>Creation date: </td><td>''' + str(result[7]) + '''</td></tr>
						<tr><td>Transaction date: </td><td>''' + str(result[8]) + '''</td></tr>
						
						<tr><td>transaction type: </td><td>'''

	#Print is_active property: 
	if(int(result[9]) == 1):						
		content += '''		<input type="radio" name="transaction_type" value="1" checked><label for="1">Deposit </label><br />
							<input type="radio" name="transaction_type" value="2"><label for="0">Withdraw </label>'''
	else:
		content += '''		<input type="radio" name="transaction_type" value="1"><label for="1">Deposit </label><br />
							<input type="radio" name="transaction_type" value="2" checked><label for="0">Withdraw </label>'''

	content += 		 '''</td></tr>


						<tr><td>Trader: supplier/costumer</td><td>
							<select name="trader_id">'''
	#Add ACTIVE warehouses select list: 
	query = "SELECT t_id, t_name FROM traders WHERE is_active = 1"

	#Check which traders to list - suppliers or costumers, accordign to the transaction type. 
	if(int(result[9]) == 1): #Means that it is a deposit transactin, hence the trader is a supplier. 
		query += " AND is_supplier = 1"
	else: #If transaction type is 2 - then it is a withdraw transaction, hence the trader is a costumer. 
		query += " AND is_costumer = 1"		

	#If the transactino is edited again after sometime, but the trader became unactive- then still print its details. 
	if(str.isdigit(str(result[10]))): 
		query += " OR t_id = %s" % (result[10])

	traders_list = conn.select_query(query)
	if(len(traders_list) == 0): 
		return "No active traders! In order to edit a transaction, you need to have at least one active suppliers or costumer, depending whether the transaction type is deposit or withdraw! "

	for trader in traders_list:
		if(trader[0] == result[10]):
			content += 			'''<option value="%s" selected>%s</option>''' %(trader[0], trader[1])
		else:
			content += 			'''<option value="%s">%s</option>''' %(trader[0], trader[1])

	content +=			'''</select>
						</td></tr>
						<tr><td>notes:</td><td><textarea name="notes">''' + str(result[11]) + '''</textarea></td></tr>
						<tr><td colspan="2"><input type="submit" value="Update Item" /></td></tr>
					</table>
				</form>
				<br />'''

	#Print available transaction status change optios: 
	content += transactions_status_change_list(transaction_id)

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

def transaction_update(transaction_id, title, reason, transaction_type, trader_id, notes):
	#UPdate transaction details. This function is activatedby a form sent by transaction_edit() function. 
	conn.execute_query("UPDATE transactions SET title = '%s' , reason = '%s' , transaction_type = '%s' , trader_id = '%s' , notes = '%s' , status = 2 , user_id_last_status = %s WHERE transaction_id = '%s' " % (title, reason, transaction_type, trader_id, notes, login.get_u_id(), transaction_id) )
	return 1

def transaction_view():
	pass




#These function will change transactions status - and change the storage. 
def transaction_close(transaction_id):
	#This function will close the transaction - and will change the items amount. 
	#IMPORTANT - in this function ther is a use with db_conn functions which do not automatically commit the changes! Only at the end of the function, if everything succeded, then a commit will be done! 
	actions = conn.select_query("SELECT item_id, amount FROM actions WHERE transaction_id = %s " % (transaction_id))
	transaction = conn.select_query_single_row("SELECT transaction_type, status FROM transactions WHERE transaction_id = %s" %(transaction_id))
	transaction_type = transaction[0]
	transaction_status = transaction[1]

	if(transaction_status not in [1,2]):
		return False

	for action in actions: 
		if(transaction_type == 1): #This transaction supposed to deposit items to the storage. 
			conn.execute_query_no_commit("UPDATE items SET amount = amount + %s WHERE item_id = %s " % (action[1], action[0]))
		elif(transaction_type ==2):  #This transaction supposed to withraw items from the storage. 
			conn.execute_query_no_commit("UPDATE items SET amount = amount - %s WHERE item_id = %s " % (action[1], action[0]))

	conn.execute_query_no_commit("UPDATE transactions SET status = 3 , user_id_finished = %s , transaction_date = '%s' WHERE transaction_id = %s " % (login.get_u_id(), date.today().strftime("%d/%m/%Y") , transaction_id))
	conn.commit()

	return True

def transaction_cancel(transaction_id):
	#Cancel transaction - only for finished transaction (status number = 3) . 
	#This function actually does the oposite of the transaction_close function. Hence - watch out for the adding and substruction of the itmes from the amount! 

	actions = conn.select_query("SELECT item_id, amount FROM actions WHERE transaction_id = %s " % (transaction_id))
	transaction = conn.select_query_single_row("SELECT transaction_type, status FROM transactions WHERE transaction_id = %s" %(transaction_id))
	transaction_type = transaction[0]
	transaction_status = transaction[1]

	if(transaction_status not in [3]):
		return False

	for action in actions: 
		if(transaction_type == 1): #This transaction is for depositing - but in cancel it should ADD BACK THE ITEMS TO THE STORAGE! 
			conn.execute_query_no_commit("UPDATE items SET amount = amount - %s WHERE item_id = %s " % (action[1], action[0]))
		elif(transaction_type ==2):  #This transaction is for withrawing - but in cancel it should SUBSTRACT THE ITEMS FROM THE STORAGE! 
			conn.execute_query_no_commit("UPDATE items SET amount = amount + %s WHERE item_id = %s " % (action[1], action[0]))

	conn.execute_query_no_commit("UPDATE transactions SET status = 4 , user_id_finished = %s WHERE transaction_id = %s " % (login.get_u_id() , transaction_id))
	conn.commit()

	return True

def transaction_open(transaction_id):
	#Open a transaction. 
	#Only finished transactions can be opened again. This requires to change the storage amounts back. 
	if(get_transaction_status(transaction_id) not in [3]):
		return 0

	#What I am actually doing is canceling the transaction which returns the storages back to its fromer amout. Then I uncancel the transaction which chnages its status back to open (2) . 
	transaction_cancel(transaction_id)
	transaction_uncancel(transaction_id)
	return 1

def transaction_delete(transaction_id):
	#Actually is just take an open (2) , created (1) or canceled (4) transaction and changes its status to deleted (5) . 
	#Both statuses are cases where no storage changes have been made! Therefore, just change the transaction_type
	transaction = conn.select_query_single_row("SELECT status FROM transactions WHERE transaction_id = %s" %(transaction_id))
	transaction_status = transaction[0]

	if(transaction_status in [1,2,4]):
		conn.execute_query("UPDATE transactions SET status = 5 , user_id_finished = %s WHERE transaction_id = %s " % (login.get_u_id() , transaction_id))
		return True
	else:
		return False

def transaction_undelete(transaction_id):
	#Chages transactions's status from delete (5) to open (2) 
	transaction = conn.select_query_single_row("SELECT status FROM transactions WHERE transaction_id = %s" %(transaction_id))
	transaction_status = transaction[0]

	if(transaction_status in [5]):
		conn.execute_query("UPDATE transactions SET status = 2 , user_id_finished = %s WHERE transaction_id = %s " % (login.get_u_id() , transaction_id))
		return True
	else:
		return False

def transaction_uncancel(transaction_id):
	#Chages transactions's status from canceled (4) to open (2) 
	transaction = conn.select_query_single_row("SELECT status FROM transactions WHERE transaction_id = %s" %(transaction_id))
	transaction_status = transaction[0]

	if(transaction_status in [4]):
		conn.execute_query("UPDATE transactions SET status = 2 , user_id_finished = %s WHERE transaction_id = %s " % (login.get_u_id() , transaction_id))
		return True
	else:
		return False

def transactions_status_change_list(transaction_id):
	#The above functinos changes the transactions' status as well as the storages amount. 
	#In the edit/view 
	status = get_transaction_status(transaction_id)
	content = "<h3>Change transaction state: </h3>"
	if(status in [1,2]): #Transaction is open. 
		content += '''<div class="button"><a href="/transactions/close/''' + str(transaction_id) + '''">Close transaction</a></div>
					<div class="button"><a href="/transactions/delete/''' + str(transaction_id) + '''">Delete transaction</a></div> ''' # Note that delete transaction is available in stauts 1 ,2 AND 4 ! 
	elif(status == 3):
		content += '''<div class="button"><a href="/transactions/open/''' + str(transaction_id) + '''">Open transaction</a></div>
					<div class="button"><a href="/transactions/cancel/''' + str(transaction_id) + '''">Cancel transaction</a></div>'''
	elif(status == 4):
		content += '''<div class="button"><a href="/transactions/uncancel/''' + str(transaction_id) + '''">Uncancel transaction</a></div>
					<div class="button"><a href="/transactions/delete/''' + str(transaction_id) + '''">Delete transaction</a></div>'''
	elif(status == 5):
		content += '''<div class="button"><a href="/transactions/undelete/''' + str(transaction_id) + '''">Undelete transaction</a></div>'''

	return content

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
	content = "<h3>Actions list: </h3>"
	#Print the table only if actions have been added: 			
	if(len(results)==0): 
		content += "no item have been added yet - so no actions can be done! Add items to the transaction in the form below: " 
	else:
		content += '''<table>
						<tr><th>action id</th><th>item id</th><th>amount</th><th>added by</th><th>notes</th><th>actions: </th></tr>'''
		for result in results: 
			content +=	 "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><a href=\"/actions/remove/%s\">delete</a> | <a href=\"/actions/edit/%s\">edit</a></td></tr>" % (result[0], translate.get_item_name(result[1]), result[2], translate.get_user_d_name(result[3]), result[4], result[0], result[0])
		content += '''</table>
						count - ''' + str(len(results))
	
	#Add a form to add another action: 
	if(get_transaction_status(transaction_id) not in [3,4,5]): #Show add actions form only if the transaction is open. 
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

#IMPORTANT - Actions can be added, edited or removed only if the transaction is open! ( status created (1) or open (2) ) 
#That is because in close status (3) the storage has been changed! Also in canceled (4) and deleted (5) status the storage shouldn't change as it is an archived stage. 

def add_action(transaction_id, item_id, amount, notes):
	#Actions can be edited only if the transaction is open - which means it status is created(1) or open (2) . 
	if(get_transaction_status(transaction_id) not in [1,2]): 
		return 0

	user_id = login.get_u_id()

	new_action_id = conn.insert_query("actions", ['item_id', 'user_id', 'transaction_id', 'amount', 'notes'], 
		[item_id, user_id, transaction_id, amount, notes])
	return new_action_id

def remove_action(action_id):
	#Actions can be edited only if the transaction is open - which means it status is created(1) or open (2) . 
	if(get_transaction_status_from_action_id(action_id) not in [1,2]): 
		return 0

	conn.execute_query("DELETE FROM actions WHERE action_id = %s" % (action_id))
	return 1

def edit_action_form(action_id):
	#Actions can be edited only if the transaction is open - which means it status is created(1) or open (2) . 
	if(get_transaction_status_from_action_id(action_id) not in [1,2]): 
		return "The transaction(%s) which this action belongs to is not open. If you want to edit this action - please open this transaction again! " % (get_transaction_status_from_action_id(action_id))


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
	#Actions can be edited only if the transaction is open - which means it status is created(1) or open (2) . 
	if(get_transaction_status_from_action_id(action_id) not in [1,2]): 
		return 0

	conn.execute_query("UPDATE actions SET item_id = '%s', amount = '%s' , notes = '%s', user_id = '%s' WHERE action_id = %s" %(item_id, amount, notes, str(login.get_u_id()) , action_id))
	return 1




#Get functions - to get fast details about transactions and actions: 
def get_transaction_status(transaction_id): 
	status = conn.select_query_single_row("SELECT status FROM transactions WHERE transaction_id = %s" % (transaction_id))
	return status[0]

def get_transaction_status_from_action_id(action_id):
	transaction_id = conn.select_query_single_row("SELECT transaction_id FROM actions WHERE action_id = %s" % (action_id))[0]
	status = conn.select_query_single_row("SELECT status FROM transactions WHERE transaction_id = %s" % (transaction_id))
	return status[0]
