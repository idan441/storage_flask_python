from flask import Flask, render_template, request, session, redirect, url_for, escape

import wh #WH = warehouses functions
import users #Users functions
import items #items functions
import transactions #transactions AND actions funcitons
import db_conn #db connection class, included also in all other modules. 
import login #Login module, which is up for logging and supplying user credentials after login. 
import reports #Reports generating functions. 
import traders #Traders functions
import translate #Translate module includes transalaetion functions which translated numeric values to their meaning AND get functions related to other modules. 
import validate #This includes validation functions to validate forms input. 

#For generating a random string for the app.secret_key - import these two modules. 
import random
import string
import os

app = Flask(__name__, template_folder="templates")

random_secret_key = ''.join(random.choice(string.ascii_lowercase) for i in range (16))
app.secret_key = random_secret_key #Used to generate sessions, in the login.py module. The value is a random string of 16 characters 




@app.route('/')
def main_page():
	if(login.is_logged_in() == 0): #Unlogged users - login
		return redirect("/login")
	return render_template('main.html', page_title="Main page:")

@app.route('/about')
def about_page():
	return render_template('about.html', page_title="About: ")

@app.route('/help')
def help_page():
	return render_template('help.html', page_title ="Help: ")



#Login micro-services
@app.route('/login', methods=['POST', 'GET'])
def login_page():
	#Check if user is loggged in
	if(login.is_logged_in()):
		return redirect('/')

	#Check if the login form was submitted
	if(request.method == 'GET'): 
		return render_template('login.html')
	else: #If it is POST , then it means the form was sent - try to relogin. 
		form_username = request.form["username"]
		form_password = request.form["password"]
		if(login.login(form_username, form_password)):
			return redirect('/') #If login success - redirect to main page
		else:
			return render_template('login.html' , warning="Wrong username or password")

@app.route('/logout')
def logout_page():
	if(login.is_logged_in() == 0): #If use is not logged-in
		return redirect('login')

	#Try to log out: 
	if(login.logout()): 
		return render_template('login.html', message="You logged out successfully! ")
	return render_template('login.html', warning="Logout failed, please try to logout again! ")

@app.route("/login/not_logged_in")
def error_not_logged_in():
	return render_template('login.html', warning="Your are not logged in - only logged in users can access this page! ")

@app.route("/login/not_admin")
def error_not_admin():
	if login.is_logged_in() ==0 :
		redirect("/login/not_logged_in")
	return render_template('index.html', warning="You have no premissions to watch this page. Only admin user can! ")




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
		form_item_name = validate.sql_escape(request.form["item_name"])
		form_amount = validate.is_number(request.form["amount"])
		form_m_unit = validate.sql_escape(request.form["m_unit"])
		form_price = validate.is_number(request.form["price"])
		form_supplier_id = validate.is_trader(request.form["supplier_id"])
		form_warehouse_id = validate.is_wh(request.form["warehouse_id"])
		form_notes = validate.sql_escape(request.form["notes"])

		items.item_add(form_item_name, form_amount, form_m_unit, form_price, form_supplier_id, form_warehouse_id, form_notes)
		return render_template('index.html', page_title="Edit item: ", message="New item was added successfully! ", content=items.items_list() )

@app.route('/items/edit/<item_id>', methods=['GET'])
def edit_item_page(item_id):	
	return render_template('index.html', page_title="Edit item: ", content=items.item_edit(item_id) )

@app.route('/items/edit', methods=['POST'])
def update_item_page():
	form_item_id = validate.is_item(request.form["item_id"])
	form_item_name = validate.sql_escape(request.form["item_name"])
	form_amount = validate.is_number(request.form["amount"])
	form_m_unit = validate.sql_escape(request.form["m_unit"])
	form_price = validate.is_number(request.form["price"])
	form_supplier_id = validate.is_trader(request.form["supplier_id"])
	form_warehouse_id = validate.is_wh(request.form["warehouse_id"])
	form_notes = validate.sql_escape(request.form["notes"])
	
	is_success = items.item_update(form_item_id, form_item_name, form_amount, form_m_unit, form_price, form_supplier_id, form_warehouse_id, form_notes)
	if(is_success):
		return render_template('index.html', page_title="Edit item: ", message="Item updated successfully! ", content=items.item_edit(form_item_id))
	return render_template('index.html', page_title="Edit item: ", warning="Item update failed", content=items.item_edit(form_item_id) )




#Transactions and actions micro-services: 
@app.route('/transactions')
@app.route('/transactions/list')
def list_transactions_page():
	if(login.is_logged_in() == 0):#Only logged in users can view this page! 
		return redirect("/login/not_logged_in")
	return render_template('index.html', page_title="Transactions list: ", content=transactions.transactions_list() )

@app.route('/transactions/new/<transaction_type>', methods=['GET'])
def new_transaction_page(transaction_type):
	if(login.is_logged_in() == 0):#Only logged in users can view this page! 
		return redirect("/login/not_logged_in")

	if(int(transaction_type) not in [1,2]):
		return "wrong value, please choose inside (1) or outside (2) "

	new_transaction_id = transactions.transaction_new(transaction_type)
	return redirect('/transactions/edit/' + str(new_transaction_id))

@app.route('/transactions/view/<transaction_id>')
def view_transaction_page(transaction_id):
	#It is for a completed transactions
	#Viewing a transaction shows information about it - but cannot allow to edit it! 	
	if(login.is_logged_in() == 0):#Only logged in users can view this page! 
		return redirect("/login/not_logged_in")

	if(int(translate.get_transaction_status(transaction_id)) in [1,2]): #OPen transaction, which has status created (1) or open (2) status - allows editing, so show them the edit forms. 
		return redirect("/transactions/edit/" + str(transaction_id))

	return render_template('index.html', page_title="View transaction: ", content=transactions.transaction_view(validate.is_transaction(transaction_id)) )

@app.route('/transactions/edit/<transaction_id>')
def edit_transaction_page(transaction_id):
	#this page allows editing transaction, adding actions to it - and eventually to apply it! 

	if(login.is_logged_in() == 0):#Only logged in users can view this page! 
		return redirect("/login/not_logged_in")

	if(int(translate.get_transaction_status(validate.is_transaction(transaction_id))) in [3, 4, 5]): #Closed transactions cannot be edited - these have status close (3) , canceled (4) or deleted (5) - so reffer them to the view mode. 
		return redirect("/transactions/view/" + str(transaction_id))

	#If information was sent from the form in this page, in order to update the transactino - then try to update it. 
	#Updating of transaction is reffered using POST method. 
	if(request.method=='POST'):
		transactions.transaction_update()

	#In case the equest to the server is with get method, then show the edit form. This form will refer to this same micro-service with POST method in order to update the transaction. 
	return render_template('index.html', page_title="Edit transaction: ", content=transactions.transaction_edit(transaction_id) )

@app.route('/transactions/update', methods=['POST'])
def update_transaction_page():
	#this page allows editing transaction, adding actions to it - and eventually to apply it! 

	if(login.is_logged_in() == 0):#Only logged in users can view this page! 
		return redirect("/login/not_logged_in")
	
	form_transaction_id = validate.is_transaction(request.form["transaction_id"])
	form_title = validate.sql_escape(request.form["title"])
	form_reason = validate.sql_escape(request.form["reason"])
	form_transaction_type = validate.is_number(request.form["transaction_type"])
	form_trader_id = validate.is_trader(request.form["trader_id"])
	form_notes = validate.sql_escape(request.form["notes"])
	
	is_success = transactions.transaction_update(form_transaction_id, form_title, form_reason, form_transaction_type, form_trader_id, form_notes)
	return redirect('/transactions/edit/' + str(form_transaction_id))


#These micro-services will change the transaction status, while changing the storage if needed to
@app.route('/transactions/close/<transaction_id>')
def close_transaction_page(transaction_id):
	#Close open transactions, later passing the user to view mode. (Because the transaction is closed and can't be edited anymore. ) 

	if(login.is_logged_in() == 0):#Only logged in users can view this page! 
		return redirect("/login/not_logged_in")

	transactions.transaction_close(validate.is_transaction(transaction_id))
	return redirect('/transactions/view/' + str(transaction_id))

@app.route('/transactions/open/<transaction_id>')
def open_transaction_page(transaction_id):
	#Close open transactions, later passing the user to view mode. (Because the transaction is closed and can't be edited anymore. ) 

	if(login.is_logged_in() == 0):#Only logged in users can view this page! 
		return redirect("/login/not_logged_in")

	transactions.transaction_open(validate.is_transaction(transaction_id))
	return redirect('/transactions/edit/' + str(transaction_id))

@app.route('/transactions/cancel/<transaction_id>')
def cancel_transaction_page(transaction_id):
	#transactions are not actually deleted from the db, but actually just changing their status, while updating the storage. 

	if(login.is_logged_in() == 0):#Only logged in users can view this page! 
		return redirect("/login/not_logged_in")

	transactions.transaction_cancel(validate.is_transaction(transaction_id))
	return redirect('/transactions/view/' + str(transaction_id))

@app.route('/transactions/uncancel/<transaction_id>')
def uncancel_transaction_page(transaction_id):
	#transactions are not actually deleted from the db, but actually just changing their status, while updating the storage. 

	if(login.is_logged_in() == 0):#Only logged in users can view this page! 
		return redirect("/login/not_logged_in")

	transactions.transaction_uncancel(validate.is_transaction(transaction_id))
	return redirect('/transactions/edit/' + str(transaction_id))

@app.route('/transactions/delete/<transaction_id>')
def delete_transaction_page(transaction_id):
	#transactions are not actually deleted from the db, but actually just changing their status, while updating the storage. 

	if(login.is_logged_in() == 0):#Only logged in users can view this page! 
		return redirect("/login/not_logged_in")

	transactions.transaction_delete(validate.is_transaction(transaction_id))
	return redirect('/transactions/view/' + str(transaction_id))

@app.route('/transactions/undelete/<transaction_id>')
def undelete_transaction_page(transaction_id):
	#transactions are not actually deleted from the db, but actually just changing their status, while updating the storage. 

	if(login.is_logged_in() == 0):#Only logged in users can view this page! 
		return redirect("/login/not_logged_in")

	transactions.transaction_undelete(validate.is_transaction(transaction_id))
	return redirect('/transactions/edit/' + str(transaction_id))



#Actions are part of transactions, and are added to a transaction. 
#Actions can only be added, edited or deleted in uncompleted transactions! 
@app.route('/actions/add', methods=['POST'])
def add_action_page():

	if(login.is_logged_in() == 0):#Only logged in users can view this page! 
		return redirect("/login/not_logged_in")

	form_transaction_id = validate.is_transaction(request.form["transaction_id"])
	form_item_id = validate.is_item(request.form["item_id"])
	form_amount = validate.is_number(request.form["amount"])
	form_notes = validate.sql_escape(request.form["notes"])
	transactions.add_action(form_transaction_id, form_item_id, form_amount, form_notes)
	return redirect('/transactions/edit/' + str(form_transaction_id))

@app.route('/actions/edit/<action_id>')
def edit_action_form_page(action_id):

	if(login.is_logged_in() == 0):#Only logged in users can view this page! 
		return redirect("/login/not_logged_in")

	return render_template('index.html', page_title="Edit action: ", content=transactions.edit_action_form(validate.is_action(action_id)) )

@app.route('/actions/edit', methods=['POST'])
def edit_action_page():

	if(login.is_logged_in() == 0):#Only logged in users can view this page! 
		return redirect("/login/not_logged_in")

	form_transaction_id = validate.is_transaction(request.form["transaction_id"])
	form_action_id = validate.is_action(request.form["action_id"])
	form_item_id = validate.is_item(request.form["item_id"])
	form_amount = validate.is_number(request.form["amount"])
	form_notes = validate.sql_escape(request.form["notes"])
	transactions.edit_action(form_transaction_id, form_item_id, form_amount, form_notes)
	return redirect('/transactions/edit/' + str(form_transaction_id))


@app.route('/actions/remove/<action_id>')
def delete_action_page(action_id):
	#An action can only be deleted in the transaction is not completed! 

	if(login.is_logged_in() == 0):#Only logged in users can view this page! 
		return redirect("/login/not_logged_in")

	conn = db_conn.db_conn()
	transaction_id_raw = conn.select_query_single_row("SELECT transaction_id FROM actions WHERE action_id = %s" % (validate.is_action(action_id)))
	transaction_id = transaction_id_raw[0]

	#delete the action - 
	transactions.remove_action(action_id)
	
	return redirect('/transactions/edit/' + str(transaction_id))




#Warehouses micro-services: 
@app.route('/warehouse/')
@app.route('/warehouse/list')
def show_warehouse_page():
	if(login.is_logged_in() == 0):#Only logged in users can view this page! 
		return redirect("/login/not_logged_in")

	return render_template('index.html', page_title="Warehouses list: ", content=wh.wh_list() )

@app.route('/warehouse/add', methods = ['POST'])
def add_warehouse_page():
	if(login.is_logged_in() == 0):#Only logged in users can view this page! 
		return redirect("/login/not_logged_in")

	form_wh_name = validate.sql_escape(request.form["wh_name"])
	form_is_active = validate.is_boolean(request.form["is_active"])
	if(wh.wh_add(form_wh_name, form_is_active)):
		return render_template('index.html', page_title="Warehouses list: " , message="Warehouse sucessfully added! " , content=wh.wh_list() )
	return render_template('index.html', page_title="Warehouses list: " , warning="Error - Warehouse wasn't added! " , content=wh.wh_list() )

@app.route('/warehouse/edit/<wh_id>')
def edit_warehouse_page(wh_id):
	if(login.is_logged_in() == 0):#Only logged in users can view this page! 
		return redirect("/login/not_logged_in")

	return render_template('index.html', page_title="Edit warehuose: " , content=wh.wh_edit(validate.is_wh(wh_id)) )

@app.route('/warehouse/update', methods = ['POST'])
def update_warehouse_page():
	if(login.is_logged_in() == 0):#Only logged in users can view this page! 
		return redirect("/login/not_logged_in")

	form_wh_id = validate.is_wh(request.form["wh_id"])
	form_wh_name = validate.sql_escape(request.form["wh_name"])
	form_is_active = validate.is_boolean(request.form["is_active"])
	if(wh.wh_update(form_wh_id, form_wh_name, form_is_active)):
		return render_template('index.html', page_title="Edit warehouse: " , message="Warehouse updated! " , content=wh.wh_edit(form_wh_id) )
	return render_template('index.html', page_title="Edit warehouse: " , warning="Update failed! " , content=wh.wh_edit(form_wh_id) )




#Users micro-services: 
@app.route('/users/')
@app.route('/users/list')
def show_users_page():
	if(login.is_logged_in_admin() == 0):#Only logged in ADMIN users can view this page! 
		return redirect("/login/not_admin")

	return render_template('index.html', page_title="Users list: ", content=users.users_list() )

@app.route('/users/add', methods = ['POST'])
def add_user_page():
	if(login.is_logged_in_admin() == 0):#Only logged in ADMIN users can view this page! 
		return redirect("/login/not_admin")

	form_u_name = validate.sql_escape(request.form["u_name"])
	form_password = validate.sql_escape(request.form["password"])
	form_d_name = validate.sql_escape(request.form["d_name"])
	return render_template('index.html', page_title="Users list: " , message=users.user_add(form_u_name, form_password, form_d_name) , content=users.users_list() )

@app.route('/users/edit/<u_id>')
def edit_user_page(u_id):
	if(login.is_logged_in_admin() == 0):#Only logged in ADMIN users can view this page! 
		return redirect("/login/not_admin")

	return render_template('index.html', page_title="Edit user: " , content=users.user_edit(validate.is_user(u_id)) )


@app.route('/users/update', methods = ['POST'])
def update_user_page():
	if(login.is_logged_in_admin() == 0):#Only logged in ADMIN users can view this page! 
		return redirect("/login/not_admin")

	form_u_id = validate.is_user(request.form["u_id"])
	form_u_name = validate.sql_escape(request.form["u_name"])
	form_d_name = validate.sql_escape(request.form["d_name"])
	form_is_active = validate.is_boolean(request.form["is_active"])
	return render_template('index.html', page_title="Edit user: " , message=users.user_update(form_u_id, form_u_name, form_is_active, form_d_name) , content=users.user_edit(form_u_id) )

@app.route('/users/change_password', methods = ['POST'])
def change_user_password_page():
	if(login.is_logged_in_admin() == 0):#Only logged in ADMIN users can view this page! 
		return redirect("/login/not_admin")

	form_u_id = validate.is_user(request.form["u_id"])
	form_new_password = validate.sql_escape(request.form["new_password"])
	if(users.user_change_password(form_u_id, form_new_password)):
		return render_template('index.html', page_title="Edit user: " , message=" Password changed succesfully! " , content=users.user_edit(form_u_id) )
	return render_template('index.html', page_title="Edit user: " , warning=" Password wasn't changed - please try again! " , content=users.user_edit(form_u_id) )



#Traders micro-services: 
@app.route('/traders/')
@app.route('/traders/list')
def show_traders_page():
	if(login.is_logged_in() == 0):#Only logged in users can view this page! 
		return redirect("/login/not_logged_in")

	return render_template('index.html', page_title="Traders list: ", content=traders.traders_list() )

@app.route('/traders/add', methods = ['GET', 'POST'])
def add_trader_page():
	if(login.is_logged_in() == 0):#Only logged in users can view this page! 
		return redirect("/login/not_logged_in")

	if(request.method == 'POST'): #Adding form was sent - then add the new trader
		form_t_name = validate.sql_escape(request.form["t_name"])
		form_contact_name = validate.sql_escape(request.form["contact_name"])
		form_phone = validate.sql_escape(request.form["phone"])
		form_address = validate.sql_escape(request.form["address"])
		form_notes = validate.sql_escape(request.form["notes"])
		form_is_active = validate.is_boolean(request.form["is_active"])
		form_is_supplier = validate.is_boolean(request.form["is_supplier"])
		form_is_costumer = validate.is_boolean(request.form["is_costumer"])

		new_trader_id = traders.add_trader(form_t_name, form_contact_name, form_phone, form_address, form_notes, form_is_active, form_is_supplier, form_is_costumer)
		return redirect('/traders/edit/' + str(new_trader_id))

	#If the request is get - then print the add new trader form
	return render_template('index.html', page_title="Add new trader: " , content=traders.add_trader_form() )


@app.route('/traders/edit/<t_id>', methods=['GET', 'POST'])
def edit_trader_page(t_id):
	if(login.is_logged_in() == 0):#Only logged in users can view this page! 
		return redirect("/login/not_logged_in")

	return render_template('index.html', page_title="Edit trader: " , content=traders.trader_edit(validate.is_trader(t_id)) )

@app.route('/traders/update', methods=['POST'])
def update_trader_page():
	if(login.is_logged_in() == 0):#Only logged in users can view this page! 
		return redirect("/login/not_logged_in")

	form_t_id = validate.is_trader(request.form["t_id"])
	form_t_name = validate.sql_escape(request.form["t_name"])
	form_contact_name = validate.sql_escape(request.form["contact_name"])
	form_phone = validate.sql_escape(request.form["phone"])
	form_address = validate.sql_escape(request.form["address"])
	form_notes = validate.sql_escape(request.form["notes"])
	form_is_active = validate.is_boolean(request.form["is_active"])
	form_is_supplier = validate.is_boolean(request.form["is_supplier"])
	form_is_costumer = validate.is_boolean(request.form["is_costumer"])
	
	is_success = traders.trader_update(form_t_id, form_t_name, form_contact_name, form_phone, form_address, form_notes, form_is_active, form_is_supplier, form_is_costumer)
	if(is_success):
		return render_template('index.html', page_title="Edit trader: ", message="trader details updated! " , content=traders.traders_list() )
	else:
		return render_template('index.html', page_title="Edit trader: ", warning="Error - update failed! " , content=traders.trader_edit(form_t_id) )




#Reports micro-services: 
@app.route('/reports/storage')
def report_storage_page():
	if(login.is_logged_in() == 0):#Only logged in users can view this page! 
		return redirect("/login/not_logged_in")

	return render_template('index.html', page_title="Storage report: ", content=reports.storage_report() )

@app.route('/reports/active_suppliers')
def report_active_suppliers_page():
	if(login.is_logged_in() == 0):#Only logged in users can view this page! 
		return redirect("/login/not_logged_in")

	return render_template('index.html', page_title="Active suppliers report: ", content=reports.active_suppliers_report() )

@app.route('/reports/transactions_by_trader', methods=['GET','POST'])
def report_transactions_by_trader_page():
	if(login.is_logged_in() == 0):#Only logged in users can view this page! 
		return redirect("/login/not_logged_in")

	if(request.args.get("t_id") != None): #If the form was sent - generate the report: 
		t_id = validate.is_trader(request.args.get('t_id'))
		return render_template('index.html', page_title="Transactions by trader report: ", content=reports.transactions_by_trader_report(t_id) )
	#Else show the form - 
	return render_template('index.html', page_title="Transactions by trader report: ", content=reports.transactions_by_trader_report_form() )

@app.route('/reports/transactions_by_item', methods=['GET','POST'])
def report_transactions_by_item_page():
	if(login.is_logged_in() == 0):#Only logged in users can view this page! 
		return redirect("/login/not_logged_in")

	if(request.args.get("i_id") != None): #If the form was sent - generate the report: 
		i_id = validate.is_item(request.args.get('i_id'))
		return render_template('index.html', page_title="Transactions by item report: ", content=reports.transactions_by_item_report(i_id) )
	#Else show the form - 
	return render_template('index.html', page_title="Transactions by item report: ", content=reports.transactions_by_item_report_form() )





if __name__ == '__main__':
	app.run( debug=os.environ.get('DEBUG', 'False'), host=os.environ.get('HOST', '0.0.0.0'), port=os.environ.get('PORT', '5000') )