from flask import Flask

#flask instance
app=Flask(__name__)

@app.route('/')
def home():
    return "Hello World"

@app.route('/products')
def products():
    return "Products Page"

@app.route('/sales')
def sales():
    return "Sales Page"

@app.route('/stock')
def stock():
    return "Stock Page"

@app.route('/dashboard')
def dashboard():
    return "Dashboard"

@app.route('/register')
def register():
    return "Registration Page"

@app.route('/login')
def login():
    return "Login Page"

#starts server to run app
app.run(debug=True)
