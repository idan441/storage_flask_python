from flask import Flask, render_template, request, session, redirect, url_for, escape

import wh #WH = warehouses functions
import users #Users functions
import items #items functions
import transactions #transactions AND actions funcitons
import db_conn #db connection class, included also in all other modules. 
import login #Login module, which is up for logging and supplying user credentials after login. 
import reports #Reports generating functions. 

app = Flask(__name__)
app.secret_key = "any random string" #Used to generate sessions, in the login.py module. 



@app.route('/')
def main_page():
	return render_template('index.html', page_title="Main page:")

@app.route('/about')
def about_page():
	content_about = '''<p>Hello, </p>
						<p>The Storage System is my first project in Python. </p>
						<p>It is built with Falsk (and django) and is supossed to be a functional storage system for small businesses or organizations. </p>
						<p>You can feel free to use it for studying, business or any other use. BE WARN THAT NO GUARNETEE IS GIVEN. Any use of this application is at your own risk. </p>

						<br />
						<p>Best regards, <br />
						&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
						&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
						&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Idan. </p>'''
	return render_template('index.html', content=content_about)



#Login micro-services
@app.route('/login', methods=['POST', 'GET'])
def login_page():
	if(request.method == 'GET'): 
		return render_template('login.html')
	else: #If it is POST , then it means the form was sent - try to relogin. 
		form_username = request.form["username"]
		form_password = request.form["password"]
		if(login.login(form_username, form_password)):
			return redirect('/') #If login success - redirect to main page
		else:
			return render_template('login.html' , message="Wrong username or password")

@app.route('/logout')
def logout_page():
	if(login.logout()): 
		return render_template('login.html', message="You logged out successfully! ")
	return render_template('login.html', message="Logout failed, please try to logout again! ")




#Items micro-services: 
@app.route('/items/')
@app.route('/items/list')
def items_list_page():
	return render_template('index.html', page_title="Items list: ", content=items.items_list() )

@app.route('/items/add', methods=['GET', 'POST'])
def items_add__page():
	if(request.method == 'GET'): #In case request method is GET, then lead to the creation form. 
		return render_template('index.html', page_title="Add item: ", content=items.item_add_form() )
	elif(request.method == 'POST'): #If request method is POST , then it means the form was sent - then add the item. 
		form_item_name = request.form["item_name"]
		form_amount = request.form["amount"]
		form_m_unit = request.form["m_unit"]
		form_price = request.form["price"]
		form_supplier_id = request.form["supplier_id"]
		form_warehouse_id = request.form["warehouse_id"]
		form_notes = request.form["notes"]
		return render_template('index.html', page_title="Add item: ", content=items.item_add(form_item_name, form_amount, form_m_unit, form_price, form_supplier_id, form_warehouse_id, form_notes) )

@app.route('/items/edit/<item_id>', methods=['GET'])
def edit_item_page(item_id):	
	return render_template('index.html', page_title="Edit item: ", content=items.item_edit(item_id) )
@app.route('/items/edit', methods=['POST'])
def update_item_page():
	form_item_id = request.form["item_id"]
	form_item_name = request.form["item_name"]
	form_amount = request.form["amount"]
	form_m_unit = request.form["m_unit"]
	form_price = request.form["price"]
	form_supplier_id = request.form["supplier_id"]
	form_warehouse_id = request.form["warehouse_id"]
	form_notes = request.form["notes"]
	return render_template('index.html', page_title="Edit item: ", content=items.item_update(form_item_id, form_item_name, form_amount, form_m_unit, form_price, form_supplier_id, form_warehouse_id, form_notes) )		




#Transactions and actions micro-services: 
@app.route('/transactions')
@app.route('/transactions/list')
def list_transactions_page():
	return render_template('index.html', page_title="Transactions list: ", content=transactions.transactions_list() )

@app.route('/transactions/new/<transaction_type>', methods=['GET'])
def new_transaction_page(transaction_type):
	if(int(transaction_type) not in [1,2]):
		return "wrong value, please choose inside (1) or outside (2) "
	new_transaction_id = transactions.transaction_new(transaction_type)
	return redirect('/transactions/edit/' + str(new_transaction_id))

@app.route('/transactions/view/<transaction_id>')
def view_transaction_page(transaction_id):
	#It is for a completed transactions
	#Viewing a transaction shows information about it - but cannot allow to edit it! 	

	#Until view is available - sned them to edit mode. 
	return redirect('/transactions/edit/' + str(transaction_id))

	return render_template('index.html', page_title="View transaction: ", content=transactions.transaction_view(transaction_id) )

@app.route('/transactions/edit/<transaction_id>')
def edit_transaction_page(transaction_id):
	#this page allows editing transaction, adding actions to it - and eventually to apply it! 

	#If information was sent from the form in this page, in order to update the transactino - then try to update it. 
	#Updating of transaction is reffered using POST method. 
	if(request.method=='POST'):
		transactions.transaction_update()

	#In case the equest to the server is with get method, then show the edit form. This form will refer to this same micro-service with POST method in order to update the transaction. 
	return render_template('index.html', page_title="Edit transaction: ", content=transactions.transaction_edit(transaction_id) )

@app.route('/transactions/update', methods=['POST'])
def update_transaction_page():
	#this page allows editing transaction, adding actions to it - and eventually to apply it! 
	
	form_transaction_id = request.form["transaction_id"]
	form_title = request.form["title"]
	form_reason = request.form["reason"]
	form_transaction_type = request.form["transaction_type"]
	form_supplier_id = request.form["supplier_id"]
	form_costumer_id = request.form["costumer_id"]
	form_notes = request.form["notes"]
	
	transactions.transaction_update(form_transaction_id, form_title, form_reason, form_transaction_type, form_supplier_id, form_costumer_id, form_notes)
	return redirect('/transactions/edit/' + str(form_transaction_id))

#These micro-services will change the transaction status, while changing the storage if needed to
@app.route('/transactions/close/<transaction_id>')
def close_transaction_page(transaction_id):
	#Close open transactions, later passing the user to view mode. (Because the transaction is closed and can't be edited anymore. ) 
	transactions.transaction_close(transaction_id)
	return redirect('/transactions/view/' + str(transaction_id))

@app.route('/transactions/open/<transaction_id>')
def open_transaction_page(transaction_id):
	#Close open transactions, later passing the user to view mode. (Because the transaction is closed and can't be edited anymore. ) 
	transactions.transaction_open(transaction_id)
	return redirect('/transactions/edit/' + str(transaction_id))

@app.route('/transactions/cancel/<transaction_id>')
def cancel_transaction_page(transaction_id):
	#transactions are not actually deleted from the db, but actually just changing their status, while updating the storage. 
	transactions.transaction_cancel(transaction_id)
	return redirect('/transactions/view/' + str(transaction_id))

@app.route('/transactions/uncancel/<transaction_id>')
def uncancel_transaction_page(transaction_id):
	#transactions are not actually deleted from the db, but actually just changing their status, while updating the storage. 
	transactions.transaction_uncancel(transaction_id)
	return redirect('/transactions/edit/' + str(transaction_id))

@app.route('/transactions/delete/<transaction_id>')
def delete_transaction_page(transaction_id):
	#transactions are not actually deleted from the db, but actually just changing their status, while updating the storage. 
	transactions.transaction_delete(transaction_id)
	return redirect('/transactions/view/' + str(transaction_id))

@app.route('/transactions/undelete/<transaction_id>')
def undelete_transaction_page(transaction_id):
	#transactions are not actually deleted from the db, but actually just changing their status, while updating the storage. 
	transactions.transaction_undelete(transaction_id)
	return redirect('/transactions/edit/' + str(transaction_id))



#Actions are part of transactions, and are added to a transaction. 
#Actions can only be added, edited or deleted in uncompleted transactions! 
@app.route('/actions/add', methods=['POST'])
def add_action_page():
	form_transaction_id = request.form["transaction_id"]
	form_item_id = request.form["item_id"]
	form_amount = request.form["amount"]
	form_notes = request.form["notes"]
	transactions.add_action(form_transaction_id, form_item_id, form_amount, form_notes)
	return redirect('/transactions/edit/' + str(form_transaction_id))

@app.route('/actions/edit/<action_id>')
def edit_action_form_page(action_id):
	return render_template('index.html', page_title="Edit action: ", content=transactions.edit_action_form(action_id) )

@app.route('/actions/edit', methods=['POST'])
def edit_action_page():
	form_transaction_id = request.form["transaction_id"]
	form_action_id = request.form["action_id"]
	form_item_id = request.form["item_id"]
	form_amount = request.form["amount"]
	form_notes = request.form["notes"]
	transactions.edit_action(form_transaction_id, form_item_id, form_amount, form_notes)
	return redirect('/transactions/edit/' + str(form_transaction_id))


@app.route('/actions/remove/<action_id>')
def delete_action_page(action_id):
	#An action can only be deleted in the transaction is not completed! 
	conn = db_conn.db_conn()
	transaction_id_raw = conn.select_query_single_row("SELECT transaction_id FROM actions WHERE action_id = %s" % (action_id))
	transaction_id = transaction_id_raw[0]

	#delete the action - 
	transactions.remove_action(action_id)
	
	return redirect('/transactions/edit/' + str(transaction_id))




#Warehouses micro-services: 
@app.route('/warehouse/')
@app.route('/warehouse/list')
def show_warehouse_page():
	return render_template('index.html', page_title="Warehouses list: ", content=wh.wh_list() )

@app.route('/warehouse/add', methods = ['POST'])
def add_warehouse_page():
	form_wh_name = request.form["wh_name"]
	form_is_active = request.form["is_active"]	
	return render_template('index.html', page_title="Warehouses list: " , warning=wh.wh_add(form_wh_name, form_is_active) , content=wh.wh_list() )

@app.route('/warehouse/edit/<wh_id>')
def edit_warehouse_page(wh_id):
	return render_template('index.html', page_title="Edit warehuose: " , content=wh.wh_edit(wh_id) )

@app.route('/warehouse/update', methods = ['POST'])
def update_warehouse_page():
	form_wh_id = request.form["wh_id"]
	form_wh_name = request.form["wh_name"]
	form_is_active = request.form["is_active"]
	return render_template('index.html', page_title="Edit warehouse: " , message=wh.wh_update(form_wh_id, form_wh_name, form_is_active) , content=wh.wh_edit(form_wh_id) )




#Users micro-services: 
@app.route('/users/')
@app.route('/users/list')
def show_users_page():
	return render_template('index.html', page_title="Users list: ", content=users.users_list() )

@app.route('/users/add', methods = ['POST'])
def add_user_page():
	form_u_name = request.form["u_name"]
	form_password = request.form["password"]
	form_d_name = request.form["d_name"]
	return render_template('index.html', page_title="Users list: " , warning=users.user_add(form_u_name, form_password, form_d_name) , content=users.users_list() )

@app.route('/users/edit/<u_id>')
def edit_user_page(u_id):
	return render_template('index.html', page_title="Edit user: " , content=users.user_edit(u_id) )

@app.route('/users/update', methods = ['POST'])
def update_user_page():
	form_u_id = request.form["u_id"]
	form_u_name = request.form["u_name"]
	form_d_name = request.form["d_name"]
	form_is_active = request.form["is_active"]
	return render_template('index.html', page_title="Edit user: " , message=users.user_update(form_u_id, form_u_name, form_is_active, form_d_name) , content=users.user_edit(form_u_id) )




#Reports micro-services: 
@app.route('/reports/storage')
def report_storage_page():
	return render_template('index.html', page_title="Storage report: ", content=reports.storage_report() )





if __name__ == '__main__':
	app.run( debug=True )