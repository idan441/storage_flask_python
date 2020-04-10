from flask import Flask, render_template, request

import wh #WH = warehouses functions
import users #Users functions
import items #items functions
import db_conn #db connection class, passed to other modules. 

app = Flask(__name__)

@app.route('/')
def main_page():
	return render_template('index.html', page_title="main page")

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

# @app.route('/items/edit/<item_id>')
# def shosssssw_item_page(item_id):
# 	return render_template('index.html', page_title="Edit item: ", content=items.item_edit(item_id) )

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