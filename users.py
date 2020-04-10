#!/bin/python
import db_conn

conn = db_conn.db_conn() #Set the connection to the database, this will be used by the following functions. 

def users_list(): 
	results = conn.select_query("SELECT u_id, u_name, is_active, is_admin FROM users")
	content = ""
	
	#It is assumed that at least one user is set, for the admin. 
	content = "<table><th>Id</th><th>name</th><th>activity</th><th>is admin</th><th>actions</td>"
	for result in results: 
		content += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><a href=\"/users/edit/%s\">edit</a></td></tr>" % ( result[0], result[1], result[2], result[3], result[0] )
	content += "</table>" 
	content += "count: " + str(len(results))
	
	content += '''<br /><br />
				<form method="post" action="/users/add">
					<table>
						<tr><td>User name: </td><td><input type="text" name="u_name" /></td></tr>
						<tr><td>Password: </td><td><input type="text" name="password" /></td></tr>
						<tr><td colspan="2"><input type="submit" value="add new user" /></td></tr>
					</table>
				</form>
				<br />
				<p>By default the new user will be active and not an admin. To change it edit the profile manually. </p>
				'''
	return content

def user_add(name, password):
	#Adds a new warehouse to the warehuoses's list
	conn.execute_query("INSERT INTO users (u_name, password, is_active, is_admin) VALUES ('%s','%s', 1, 0)" % (name, password))
	return " new user added! "

def user_edit(u_id):
	#Adds a new warehouse to the warehuoses's list
	result = conn.select_query_single_row("SELECT u_id, u_name, is_active, is_admin FROM users WHERE u_id = %s" % (u_id) )

	content = '''<form method="post" action="/users/update">
					<table>
						<tr><td>User Id: </td><td><input type="hidden" name="u_id" value="''' + str(result[0]) + '''" />''' + str(result[0]) + '''</td></tr>
						<tr><td>User name: </td><td><input type="text" name="u_name" value="''' + str(result[1]) + '''" /></td></tr>
						<tr><td> Is it active? </td><td><input type="text" name="is_active" value="''' + str(result[2]) + '''" /></td></tr>
						<tr><td> Is it admin? </td><td>''' + str(result[3]) + '''</td></tr>
						<tr><td colspan="2"><input type="submit" value="Update user" /></td></tr>
					</table>
				</form>
				<br />
				<p>Due to fact that the user might have done archived actions, users cannot be deleted. Instead, you can deactivate them</p>
				'''
	return content

def user_update(u_id, u_name, is_active):
	#Adds a new warehouse to the warehuoses's list
	conn.execute_query("UPDATE users SET u_name = '%s' , is_active = '%s' WHERE u_id = '%s' " % (u_name, is_active, u_id))
	return "user %s(%s) updated!" % (u_name, u_id)
