#!/bin/python
import db_conn

conn = db_conn.db_conn() #Set the connection to the database, this will be used by the following functions. 

def users_list(): 
	results = conn.select_query("SELECT wh_id, wh_name, is_active FROM warehouses")
	content = ""
	
	if(len(results)==0): 
		content += "no warehouses have been added yet! " 
	else: 
		content = "<table><th>Id</th><th>name</th><th>activity</th><th>actions</td>"
		for result in results: 
			content += "<tr><td>%s</td><td>%s</td><td>%s</td><td><a href=\"/warehouse/delete/%s\">delete</a> | <a href=\"/warehouse/edit/%s\">edit</a></td></tr>" % ( result[0], result[1], result[2], result[0], result[0] )
		content += "</table>" 
		content += "count: " + str(len(results))
	
	content += '''<br /><br />
				<form method="post" action="/warehouse/add">
					<table>
						<tr><td>Warehouse name: </td><td><input type="text" name="wh_name" /></td></tr>
						<tr><td> Is it active? </td><td><input type="text" name="is_active" /></td></tr>
						<tr><td colspan="2"><input type="submit" value="add" /></td></tr>
					</table>
				</form>'''
	return content


def users_add(name, is_active):
	#Adds a new warehouse to the warehuoses's list
	conn.execute_query("INSERT INTO warehouses (wh_name, is_active) VALUES ('%s','%s')" % (name, is_active))
	return " warehouses added! "

def users_edit(wh_id):
	#Adds a new warehouse to the warehuoses's list
	result = conn.select_query_single_row("SELECT wh_id, wh_name, is_active FROM warehouses WHERE wh_id = %s" % (wh_id) )

	content = '''<form method="post" action="/warehouse/update">
					<table>
						<tr><td>Warehouse Id: </td><td><input type="hidden" name="wh_id" value="''' + str(result[0]) + '''" />''' + str(result[0]) + '''</td></tr>
						<tr><td>Warehouse name: </td><td><input type="text" name="wh_name" value="''' + str(result[1]) + '''" /></td></tr>
						<tr><td> Is it active? </td><td><input type="text" name="is_active" value="''' + str(result[2]) + '''" /></td></tr>
						<tr><td colspan="2"><input type="submit" value="Update" /></td></tr>
					</table>
				</form>'''
	return content

def users_update(wh_id, wh_name, is_active):
	#Adds a new warehouse to the warehuoses's list
	conn.execute_query("UPDATE warehouses SET wh_name = '%s' , is_active = '%s' WHERE wh_id = '%s' " % (wh_name, is_active, wh_id))
	return "Warehouse %s(%s) updated!" % (wh_name, wh_id)

def users_delete(wh_id):
	#Adds a new warehouse to the warehuoses's list
	conn.execute_query("DELETE FROM warehouses WHERE wh_id = '%s' " % (wh_id))
	return " warehouses removed! "

