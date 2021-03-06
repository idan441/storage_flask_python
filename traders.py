#!/bin/python
import db_conn
import translate
import login

conn = db_conn.db_conn() #Set the connection to the database, this will be used by the following functions. 



def traders_list(): 
	#Prints traders list
	results = conn.select_query("SELECT t_id, t_name, is_active, is_supplier, is_costumer FROM traders")
	content = ""

	if len(results) > 0 :
		content += "<table><th>Id</th><th>name</th><th>activity</th><th>Roles</th><th>actions</td>"
		for result in results: 
			content += "<tr><td>%s</td><td>%s</td><td>%s</td><td>supplier - %s<br />costumer - %s</td><td><a href=\"/traders/edit/%s\">edit</a></td></tr>" % ( result[0], result[1], translate.translate_active_state(result[2]), translate.translate_active_state(result[3]), translate.translate_active_state(result[4]), result[0] )
		content += '''</table>
						count: ''' + str(len(results)) 
	else:
		content += "No traders have been added yet! "

	content +=	 '''<br /><br />
					<div class="button"><a href="/traders/add">Add a new trader</a></div>'''

	return content

def add_trader_form():	
	#Print a form for adding a new trader. The form redirect to an address which reffers to the add_trader() funciton below this function. 
	content = '''<h3>Add a new trader: </h3>
				<form method="post" action="/traders/add">
					<table>
						<tr><td>Trader name: </td><td><input type="text" name="t_name" /></td></tr>
						<tr><td>Contact name: </td><td><input type="text" name="contact_name" /></td></tr>
						<tr><td>Phone number: </td><td><input type="text" name="phone" /></td></tr>
						<tr><td>Address: </td><td><input type="text" name="address" /></td></tr>
						<tr><td>Is active: </td><td>
												<input type="radio" name="is_active" value="1" checked><label for="1">Yes </label><br />
												<input type="radio" name="is_active" value="0"><label for="0">No </label>
											</td></tr>
						<tr><td>Is supplier: </td><td>
												<input type="radio" name="is_supplier" value="1" checked><label for="1">Yes </label><br />
												<input type="radio" name="is_supplier" value="0"><label for="0">No </label>
											</td></tr>
						<tr><td>Is costumer: </td><td>
												<input type="radio" name="is_costumer" value="1" checked><label for="1">Yes </label><br />
												<input type="radio" name="is_costumer" value="0"><label for="0">No </label>
											</td></tr>
						<tr><td>notes:</td><td><textarea name="notes"></textarea></td></tr>
						<tr><td colspan="2"><input type="submit" value="add new trader" /></td></tr>
					</table>
				</form>
				<br />'''
	return content

def add_trader(t_name, contact_name, phone, address, notes, is_active, is_supplier, is_costumer):
	#Add a new trader to the database and returns the new trader id. This function accepts infromation from the form add_trader_from() function above. 
	new_trader_id = conn.insert_query("traders", ['t_name', 'contact_name', 'phone', 'address', 'notes', 'is_active', 'is_supplier', 'is_costumer'], [t_name, contact_name, phone, address, notes, is_active, is_supplier, is_costumer])
	return new_trader_id

def trader_edit(t_id):
	#This function prints an edit form with the trader's details. (trader ID is needed - t_id)
	result = conn.select_query_single_row("SELECT t_name, contact_name, phone, address, notes, is_active, is_supplier, is_costumer, t_id FROM traders WHERE t_id = %s" % (t_id) )

	content = '''<form method="post" action="/traders/update">
					<table>
						<tr><td>Trader ID: </td><td><input type="hidden" name="t_id" value="''' + str(result[8]) + '''" />''' + str(result[8]) + '''</td></tr>
						<tr><td>Trader name: </td><td><input type="text" name="t_name" value="''' + result[0] + '''" /></td></tr>
						<tr><td>Contact name: </td><td><input type="text" name="contact_name" value="''' + result[1] + '''" /></td></tr>
						<tr><td>Phone number: </td><td><input type="text" name="phone" value="''' + result[2] + '''" /></td></tr>
						<tr><td>Address: </td><td><input type="text" name="address" value="''' + result[3] + '''" /></td></tr>
						<tr><td>Is active: </td><td>'''

	#Print is_active property: 
	if(int(result[5]) == 1):
		content += '''		<input type="radio" name="is_active" value="1" checked><label for="1">Active </label><br />
							<input type="radio" name="is_active" value="0"><label for="0">Not active </label>'''
	else:
		content += '''		<input type="radio" name="is_active" value="1"><label for="1">Active </label><br />
							<input type="radio" name="is_active" value="0" checked><label for="0">Not active </label>'''

	content += 		'''</td></tr>
						<tr><td>Is supplier: </td><td>'''

	#Print is_supplier property: 
	if(int(result[6]) == 1):
		content += '''		<input type="radio" name="is_supplier" value="1" checked><label for="1">Active </label><br />
							<input type="radio" name="is_supplier" value="0"><label for="0">Not active </label>'''
	else:
		content += '''		<input type="radio" name="is_supplier" value="1"><label for="1">Active </label><br />
							<input type="radio" name="is_supplier" value="0" checked><label for="0">Not active </label>'''

	content += 		'''</td></tr>
						<tr><td>Is costumer: </td><td>'''

	#Print is_supplier property: 
	if(int(result[7]) == 1):
		content += '''		<input type="radio" name="is_costumer" value="1" checked><label for="1">Active </label><br />
							<input type="radio" name="is_costumer" value="0"><label for="0">Not active </label>'''
	else:
		content += '''		<input type="radio" name="is_costumer" value="1"><label for="1">Active </label><br />
							<input type="radio" name="is_costumer" value="0" checked><label for="0">Not active </label>'''

	content += 		 '''</td></tr>
						<tr><td>notes:</td><td><textarea name="notes">''' + result[4] + '''</textarea></td></tr>
						<tr><td colspan="2"><input type="submit" value="Update user" /></td></tr>
					</table>
				</form>

				<br />
				<h3>Reports: </h3>
				<a href="/reports/transactions_by_trader?t_id=''' + t_id + '''">Transactions done by this trade</a>'''

	return content

def trader_update(t_id, t_name, contact_name, phone, address, notes, is_active, is_supplier, is_costumer):
	#Updates an existing trader. This function is being called from main.py after sending the form generated from the funciton above. 
	conn.execute_query("UPDATE traders SET t_name = '%s' , contact_name = '%s' , phone = '%s' , address = '%s' , notes = '%s' , is_active = '%s' , is_supplier = '%s' , is_costumer = '%s' WHERE t_id = '%s' " % (t_name, contact_name, phone, address, notes, is_active, is_supplier, is_costumer, t_id))
	return 1

