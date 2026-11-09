import psycopg2

#establishing a db connection
conn = psycopg2.connect(host='localhost',port=5433,user='postgres',password='Katisaa@2022',dbname='myduka_db')

#creating cur object to perform db operations
cur=conn.cursor()

def get_products():
    cur.execute("select*from products")
    products_data=cur.fetchall()
    return products_data

products_data=get_products()
print(products_data)

def insert_products():
      cur.execute("insert into products(name,buying_price,selling_price)values('asus lapop',40000,50000)")
      conn.commit()
    

insert_products()
products_data=get_products()
print(products_data)

def get_sales():
     cur.execute("select*from sales")
     sales_data=cur.fetchall()
     return sales_data
sales_data=get_sales()
print(sales_data)

def insert_sales():
     cur.execute("insert into sales(pid,quantity)values(001,2235)")
     cur.execute("insert into sales(pid,quantity)values(002,1100)")  
     conn.commit()

insert_sales()
sales_data=get_sales()
print(sales_data)

# Reusable function
def insert_products(prod_details):
     cur.execute("insert into products(name,buying_price,selling_price)values(%s,%s,%s)",prod_details)
     conn.commit()

product1=('iphone 14',50000,60000)
product2=('rice',200,250)
product3=('milk',65,80)
product4=('samgung tv',34000,42000)
insert_products(product1)
insert_products(product2)
insert_products(product3)
insert_products(product4)

products_data=get_products()
print(products_data)

def fetch_sales():
     cur.execute("select*from sales")
     sales_data=cur.fetchall()
     return sales_data

def insert_sales(sales_details):
     cur.execute("insert into sales(pid,quantity)values(%s,%s)",sales_details)
     conn.commit()

sale1=(2,45)
sale2=(1,10)
insert_sales(sale1)
insert_sales(sale2)

sales_data=fetch_sales()
print(sales_data)

def get_sales_per_product():
    cur.execute(
    """
        select products.name as p_name,sum(products.selling_price * sales.quantity) as total_sales
        from sales join products on products.id = sales.pid group by p_name;
    """)
    sales_per_product = cur.fetchall()
    return sales_per_product

sales_per_product = get_sales_per_product()
print(sales_per_product)

def get_sales_per_day():
    cur.execute("""
        SELECT
            DATE(sales.created_at) AS sale_day,
            SUM(products.selling_price * sales.quantity) AS total_sales FROM sales JOIN products ON products.id = sales.pid GROUP BY sale_day ORDER BY sale_day;
    """)

    sales_per_day = cur.fetchall()
    return sales_per_day

sales_per_day = get_sales_per_day()
print(sales_per_day)

def get_profit_per_product():
    cur.execute("""
        SELECT
            products.name AS p_name,
            SUM((products.selling_price - products.buying_price) * sales.quantity) AS total_profit
        FROM sales
        JOIN products ON products.id = sales.pid
        GROUP BY products.id, products.name
        ORDER BY total_profit DESC;
    """)

    profit_per_product=cur.fetchall()
    return profit_per_product

profit_per_product=get_profit_per_product()
print(profit_per_product)

def get_profit_per_day():
     cur.execute("""   
     SELECT
            DATE(sales.created_at) AS sale_day,SUM((products.selling_price - products.buying_price)* sales.quantity) AS total_profit FROM sales 
            JOIN products ON products.id = sales.pid GROUP BY sale_day ORDER BY sale_day;
""")

     profit_per_day=cur.fetchall()
     return profit_per_day

profit_per_day=get_profit_per_day()
print(profit_per_day)

