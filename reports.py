#!/bin/python
from datetime import date
import db_conn
import translate
import login


conn = db_conn.db_conn() #Set the connection to the database, this will be used by the following functions. 

def storage_report():
	#Prints a report with all storage, including amounts and warehouse: 
	items = conn.select_query("SELECT item_id, item_name, m_unit, amount, warehouse_id, notes FROM items")

	content =   '''<table>
						<tr><th>Item ID</th><th>Item name</th><th>Amount</th><th>Warehouse / Location</th><th>Notes</th></tr>'''

	for item in items:
		content += '''<tr><td>%s</td><td>%s</td><td>%s %s</td><td>%s</td><td>%s</td></tr>''' % (item[0], item[1], item[3], item[2], translate.get_warehouse_name(item[4]), item[5])

	content += '''</table>
					Total items on list: ''' + str(len(items)) + ''' 
					<br />Report generated at: ''' + str(date.today().strftime("%d/%m/%Y")) + '''
					<br />Generated by: ''' + login.get_d_name()

	return content

def active_suppliers_report():
	#Prints all active suppliers and their contact details
	suppliers = conn.select_query("SELECT t_id, t_name, contact_name, phone, address FROM traders WHERE is_supplier = 1 AND is_active = 1")

	content =   '''<table>
						<tr><th>Supplier ID</th><th>Name</th><th>Contact_name</th><th>Phone num.</th><th>Address</th></tr>'''

	for supplier in suppliers:
		content += '''<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>''' % (supplier[0], supplier[1], supplier[2], supplier[3], supplier[4])

	content += '''</table>
					Total items on list: ''' + str(len(suppliers)) + ''' 
					<br />Report generated at: ''' + str(date.today().strftime("%d/%m/%Y")) + '''
					<br />Generated by: ''' + login.get_d_name()

	return content

def transactions_by_trader_report_form():
	#Prints a form which sends details for the transactions_by_trader_reports() functions below. 
	content = '''<p>Please choose a trader: </p>
				<form method="get" action="/reports/transactions_by_trader">
					<table>
						<tr><th>Trader name: </th><td>
							<select name="t_id">'''

	traders_list = conn.select_query("SELECT t_id, t_name FROM traders")
	if(len(traders_list) == 0):
		return "No traders have been created! Before using this report you must create at list one trader! <a href=""/traders"">Click here to create a new trader</a>"

	for trader in traders_list:
		content += 			'''<option value="%s">%s</option>''' %(trader[0], trader[1])

	content +=		'''		</select></td>
						<tr><td colspan="2"><input type="submit" value="Generate report" /></td>
					</table>'''
	return content

def transactions_by_trader_report(t_id):
	#Prints all transactions associated with a specific trader

	#Print the trader's details - 
	trader = conn.select_query_single_row("SELECT t_id, t_name, notes, contact_name, phone, address FROM traders WHERE t_id = %s" % (t_id))
	
	content = '''<table>
				<tr><th>Trader name:</th><th>Trader ID: </th></tr>
				<tr><td>%s</td><td>%s</td></tr>
				</table>''' % (trader[1] , trader[0])

	content += '''<table>
					<tr><th colspan="3">Indications: </th></tr>
					<tr><th>Activity:</th><th>Supplier:</th><th>Costumer</th></tr>
					<tr>''' 
	if(translate.is_trader_active(t_id)):
		content += "<td>Yes</td>"
	else:
		content += "<td>No</td>"

	if(translate.is_trader_supplier(t_id)):
		content += "<td>Yes</td>"
	else:
		content += "<td>No</td>"

	if(translate.is_trader_active(t_id)):
		content += "<td>Yes</td>"
	else:
		content += "<td>No</td>"

	content += '''</tr>
					</table>

					<table>
					<tr><th colspan="3">Contact details: </th></tr>
					<tr><th>contact name</th><th>Phone number</th><th>Address</th></tr>
					<tr><td>%s</td><td>%s</td><td>%s</td></tr>''' % (trader[3], trader[4], trader[5])
	content += '''<tr><td colspan="3">Notes: %s</td></tr></table><br />''' % (trader[2])

	#Print the transactions: 
	transactions = conn.select_query("SELECT transaction_id, title, status, transaction_type, creation_date, transaction_date FROM transactions WHERE trader_id = %s" % (t_id))

	content +=   '''<h4> Transactions done by this trader: </h4>
					<table>
						<tr><th>Transaction ID</th><th>Title</th><th>Status</th><th>Transaction Type<th>Creation date</th><th>Transaction date</th></tr>'''

	for transaction in transactions:
		content += '''<tr><td><a href="/transactions/edit/%s">%s</a></td><td><a href="/transactions/edit/%s">%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>''' % (transaction[0], transaction[0], transaction[0], transaction[1], translate.translate_status(transaction[2]), translate.translate_transaction_type(transaction[3]), transaction[4], transaction[5])

	content += '''</table>
					Total transactions: ''' + str(len(transactions)) + ''' 
					<br />Report generated at: ''' + str(date.today().strftime("%d/%m/%Y")) + '''
					<br />Generated by: ''' + login.get_d_name()

	return content

def transactions_by_item_report_form():
	#Prints a form which sends details for the transactions_by_trader_reports() functions below. 
	content = '''<p>Please choose a name: </p>
				<form method="get" action="/reports/transactions_by_item">
					<table>
						<tr><th>Item name: </th><td>
							<select name="i_id">'''

	items_list = conn.select_query("SELECT item_id, item_name FROM items")
	if(len(items_list) == 0):
		return "No items have been created! Before using this report you must create at list one item! <a href=""/items"">Click here to create a new item</a>"
	for item in items_list:
		content += 			'''<option value="%s">%s</option>''' %(item[0], item[1])

	content +=		'''		</select></td>
						<tr><td colspan="2"><input type="submit" value="Generate report" /></td>
					</table>'''
	return content

def transactions_by_item_report(i_id):
	#Prints all transactions which included a specific item. 
	
	#Print items details: 
	item = conn.select_query_single_row("SELECT item_id, item_name, amount, m_unit, price, warehouse_id, supplier_id, notes FROM items WHERE item_id = %s" % (i_id))
	
	content = '''<table>
				<tr><th>Item name:</th><th>Item ID: </th></tr>
				<tr><td>%s</td><td>%s</td></tr>
				</table>''' % (item[1] , item[0])

	content += '''<table>
					<tr><th colspan="5">Storage properties: </th></tr>
					<tr><th>Amount:</th><th>Measurement unit:</th><th>Price: </th><th>Warehouse: </th><th>Supplier: </th></tr>
					<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>
					<tr><td colspan="5">Notes: %s</td></tr>
				</table>''' % (item[2], item[3], item[4], translate.get_warehouse_name(item[5]), translate.get_trader_name(item[6]), item[7])

	#Print the transactions which has an action with the item's id. 
	actions = conn.select_query("SELECT action_id, transaction_id, amount, user_id FROM actions WHERE item_id = %s" % (i_id))

	content +=   '''<h4>transactions list which has this item: </h4>
					<table>
						<tr><th>action ID</th><th>Transaction Title(Transaction ID)</th><th>Transaction Type</th><th>Amount</th><th>Action added by</tr>'''

	for action in actions:
		content += '''<tr><td>%s</td><td><a href="/transactions/edit/%s">%s(%s)</a></td><td>%s</td><td>%s (%s)</td><td><a href="/users/edit/%s">%s</a></td></tr>''' % (action[0], action[1], translate.get_transaction_title(action[1]), action[1], translate.translate_transaction_type(translate.get_transaction_type(action[1])), action[2], item[3], action[3], translate.get_user_d_name(action[3]))

	content += '''</table>
					Total items on list: ''' + str(len(actions)) + ''' 
					<br />Report generated at: ''' + str(date.today().strftime("%d/%m/%Y")) + '''
					<br />Generated by: ''' + login.get_d_name() + '''
					<br />Please note that the item's amount displayed in the top of the report, and in the listed transactions - is right at the moment of generating this report. '''

	return content

