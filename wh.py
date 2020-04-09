#!/bin/python
import db_conn



def wh_list(conn): 
	results = conn.select_query("SELECT wh_id, wh_name, is_active FROM warehouses")
	content = ""
	
	if(len(results)==0): 
		content += "no warehouses have been added yet! " 
	else: 
		content = "<table><th>Id</th><th>name</th><th>activity</th>"
		for result in results: 
			content += "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % ( result[0], result[1], result[2] )
		content += "</table>" 
		content += "count: " + str(len(results))
	
		content += '''<form method="post" action="/warehouse/add">
						<table>
							<tr><td>Warehouse name: </td><td><input type="text" name="wh_name" /></td></tr>
							<tr><td> Is it active? </td><td><input type="text" name="is_active" /></td></tr>
							<tr><td colspan="2"><input type="submit" value="add" /></td></tr>
						</table>
					</form>'''
	return content


def wh_add(conn, name, is_active):
	#Adds a new warehouse to the warehuoses's list
	conn.execute_query("INSERT INTO warehouses (wh_name, is_active) VALUES ('%s','%s')" % (name, is_active))
	return " warehouses added! "