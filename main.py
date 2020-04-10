from flask import Flask, render_template, request

import wh #WH = warehouses functions
import users #Users functions
import db_conn #db connectino class, passed to other modules. 

app = Flask(__name__)

@app.route('/')
def main_page():
	return render_template('index.html', page_title="main page")

@app.route('/items/')
@app.route('/items/list')
def items_list_page():
	return 'Items list page'

@app.route('/item/<item_id>')
def show_item_page():
	return 'welcome to the main page! '


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