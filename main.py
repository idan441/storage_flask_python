from flask import Flask, render_template, request

import wh #WH warehouses functions
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
	conn = db_conn.db_conn()
	return render_template('index.html', page_title="Warehouses list: ", content=wh.wh_list(conn) )

@app.route('/warehouse/add', methods = ['POST'])
def add_warehouse_page():
	form_wh_name = request.form["wh_name"]
	form_is_active = request.form["is_active"]
	conn = db_conn.db_conn()
	
	return render_template('index.html', page_title="Warehouses list: " , warning=wh.wh_add(conn, form_wh_name, form_is_active) , content=wh.wh_list(conn) )

@app.route('/warehouse/update/<wh_id>')
def update_warehouse_page(wh_id):
	return 'update warehouse page! ' + wh_id

@app.route('/warehouse/delete/<wh_id>')
def delete_warehouse_page(wh_id):
	form_wh_id = wh_id
	conn = db_conn.db_conn()
	return render_template('index.html', page_title="Warehouses list: " , warning=wh.wh_delete(conn, form_wh_id) , content=wh.wh_list(conn) )




@app.route('/users/')
@app.route('/users/list')
def users_list_page():
	return 'add warehouse page! '






if __name__ == '__main__':
	app.run( debug=True )