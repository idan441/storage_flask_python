from flask import Flask, render_template
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
   return 'warehouse page! '

@app.route('/warehouse/add')
def add_warehouse_page():
   return 'add warehouse page! '

@app.route('/users/')
@app.route('/users/list')
def add_warehouse_page():
   return 'add warehouse page! '






if __name__ == '__main__':
   app.run( debug=True)