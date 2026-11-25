from flask import Flask, render_template,request,redirect,url_for,flash,session
from database import get_products,insert_products
from database import get_sales,insert_sales,get_profit_per_day,get_profit_per_product,get_sales_per_day,get_sales_per_product,insert_user,check_user_exists
from database import get_stock,insert_stock
from flask_bcrypt import  Bcrypt
from functools import wraps

 

#flask instance
app=Flask(__name__)
app.secret_key='Katisaa@2022'

#bcrypt instance
bcrypt = Bcrypt(app)

@app.route('/') #Decorator Function
def home():  # View function 
    return render_template('index.html')

def login_required(f):
    @wraps(f)
    def protected(*args,**kwargs):
        if 'email' not in session:
            return redirect(url_for('login'))
        return f(*args,**kwargs)
    return protected

@app.route('/products')
@login_required
def products():
    products_data = get_products()
    return render_template('products.html',products_data = products_data)

@app.route('/add_products',methods=['GET','POST'])
def add_products():
    if request.method =="POST":
        product_name=request.form['p_name']
        buying_price=request.form['b_price']
        selling_price=request.form['s_price']

        new_product=(product_name,buying_price,selling_price)
        insert_products(new_product)
        flash ("Products added successfully",'success')
    return redirect(url_for('products'))

@app.route('/sales')
@login_required
def sales():
    sales_data = get_sales()
    products_data=get_products()
    return render_template('sales.html',sales_data = sales_data, products_data=products_data)


@app.route('/add_sales', methods=['GET', 'POST'])
def add_sales():
    if request.method == "POST":
        product_id = request.form['p_id']
        sales_quantity = request.form['st_quantity']

        new_sales = (product_id, sales_quantity)
        insert_sales(new_sales)

        flash("Sales added successfully", "success")

        return redirect(url_for('sales'))

    return render_template('add_sales.html')

@app.route('/stock')
def stock():
    stock_data = get_stock()
    products_data=get_products()
    return render_template('stock.html',stock_data = stock_data,products_data=products_data)

@app.route('/add_stock',methods=['GET','POST'])
def add_stock():
    if request.method =="POST":
        product_id=request.form['p_id']
        stock_quantity=request.form['st_quantity']
        
        new_stock=(product_id,stock_quantity)
        insert_stock(new_stock)
        flash ("Stock added successfully", 'success')
    return redirect(url_for('stock'))


@app.route('/dashboard')
def dashboard():

    product_sales = get_sales_per_product()
    daily_sales = get_sales_per_day()

    product_profit = get_sales_per_product()
    daily_profit = get_profit_per_day()

    products_names = [i[0] for i in product_sales]
    sales_p = [float(i[1]) for i in product_sales]
    profit_p = [float(i[1]) for i in product_profit]

    days = [str(i[0]) for i in daily_sales]
    sales_day = [float(i[1]) for i in daily_sales]
    profit_day = [float(i[1]) for i in daily_profit]

    return render_template(
        'dashboard.html',product_names=products_names,sales_p=sales_p,profit_p=profit_p,
        days=days,sales_day=sales_day,profit_day=profit_day
    )

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == "POST":
        full_name=request.form ['name']
        email=request.form['email']
        phone= request.form['phone']
        password = request.form['password']

        existing_user=check_user_exists(email)

    if existing_user :
            flash("User already exists,login instead",'danger')
            return redirect(url_for('login'))
  
    else:
          hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
          new_user=(full_name,email,phone,hashed_password)
          insert_user(new_user)
          flash("User registered successfully")
          return redirect(url_for('login'))


    return render_template('register.html')




@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        existing_user = check_user_exists(email) 

        if not existing_user:
            flash("User with this email doesn't exist,register instead",'danger')
            return redirect(url_for('register'))
        else:
            check_password = bcrypt.check_password_hash(existing_user[-1],password)

            if check_password:
                flash("Logged in successfully",'success')
                session['email'] = email
                redirect(url_for('dashboard'))
            else:
                flash("Incorrect password ,try again",'danger')
                return redirect(url_for('login'))


    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email',None)
    flash('Logged out successfully')
    return redirect(url_for('login'))

#starts server to run app
app.run(debug=True)
