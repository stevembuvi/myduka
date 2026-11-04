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