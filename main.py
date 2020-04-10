from flask import Flask, render_template, request

import wh #WH = warehouses functions
import users #Users functions
import items #items functions
import db_conn #db connection class, passed to other modules. 

app = Flask(__name__)

@app.route('/')
def main_page():
	return render_template('index.html', page_title="main page")




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
def list_transactions_page(item_id):	
	return render_template('index.html', page_title="Transactions list: ", content=items.item_edit(item_id) )

@app.route('/transactions/add')
def add_transaction_page(item_id):	
	return render_template('index.html', page_title="Add transaction: ", content=items.item_edit(item_id) )

@app.route('/transactions/view/<transaction_id>')
def view_transaction_page(item_id):
	#It is for a completed transactions
	#Viewing a transaction shows information about it - but cannot allow to edit it! 	
	return render_template('index.html', page_title="View transaction: ", content=items.item_edit(item_id) )

@app.route('/transactions/edit/<transaction_id>')
def edit_transaction_page(item_id):	
	#It allows editing transaction, adding actions to it - and eventually to apply it! 
	return render_template('index.html', page_title="Edit transaction: ", content=items.item_edit(item_id) )

@app.route('/transactions/delete/<transaction_id>')
def delete_transaction_page(item_id):
	#transactions are not actually deleted from the db, but actually just changing their status, while updating the storage. 
	return render_template('index.html', page_title="Delete transaction: ", content=items.item_edit(item_id) )

#Actions are part of transactions, and are added to a transaction. 
#Actions can only be added, edited or deleted in uncompleted transactions! 
@app.route('/actions/add/<transaction_id>')
def add_action_page(item_id):	
	return render_template('index.html', page_title="Add action: ", content=items.item_edit(item_id) )

@app.route('/actions/edit/<action_id>')
def edit_action_page(item_id):	
	return render_template('index.html', page_title="Edit action: ", content=items.item_edit(item_id) )

@app.route('/actions/delete/<action_id>')
def delete_action_page(item_id):
	#An action can only be deleted in the transaction is not completed! 
	return render_template('index.html', page_title="Delete action: ", content=items.item_edit(item_id) )




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

@app.route('/warehouse/delete/<wh_id>')
def delete_warehouse_page(wh_id):
	form_wh_id = wh_id
	return render_template('index.html', page_title="Warehouses list: " , warning=wh.wh_delete(form_wh_id) , content=wh.wh_list() )




#Users micro-services: 
@app.route('/users/')
@app.route('/users/list')
def show_users_page():
	return render_template('index.html', page_title="Users list: ", content=users.users_list() )

@app.route('/users/add', methods = ['POST'])
def add_user_page():
	form_u_name = request.form["u_name"]
	form_password = request.form["password"]	
	return render_template('index.html', page_title="Users list: " , warning=users.user_add(form_u_name, form_password) , content=users.users_list() )

@app.route('/users/edit/<u_id>')
def edit_user_page(u_id):
	return render_template('index.html', page_title="Edit user: " , content=users.user_edit(u_id) )

@app.route('/users/update', methods = ['POST'])
def update_user_page():
	form_u_id = request.form["u_id"]
	form_u_name = request.form["u_name"]
	form_is_active = request.form["is_active"]
	return render_template('index.html', page_title="Edit user: " , message=users.user_update(form_u_id, form_u_name, form_is_active) , content=users.user_edit(form_u_id) )






if __name__ == '__main__':
	app.run( debug=True )