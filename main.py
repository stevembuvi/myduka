from flask import Flask, render_template
from database import get_products
from database import get_sales
from database import get_stock

#flask instance
app=Flask(__name__)

@app.route('/') #Decorator Function
def home():  # View func
    return render_template('index.html')

@app.route('/products')
def products():
    products_data = get_products()
    return render_template('products.html',products_data = products_data)

@app.route('/sales')
def sales():
    sales_data = get_sales()
    return render_template('sales.html',sales_data = sales_data )

@app.route('/stock')
def stock():
    stock_data = get_stock()
    return render_template('stock.html',stock_data = stock_data)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

#starts server to run app
app.run(debug=True)
