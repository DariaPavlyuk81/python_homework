import sqlite3

conn = sqlite3.connect("../db/lesson.db")
cursor = conn.cursor()

# print("connected to db/lesson/db")

#Task1
# SELECT customer_name,city
# FROM customers


# cursor.execute('''
# SELECT customer_name,city
# FROM customers

# ''')

# for row in cursor.fetchall():
#     print(row)

# conn.close()

# SELECT employees.employee_id,
# employees.last_name,
# products.product_name
# FROM employees
# JOIN orders ON employees.employee_id = orders.employee_id
# JOIN products ON line_items.product_id = products.product_id
# LIMIT 5;

# query = '''
# SELECT 
#   employees.employee_id,
#   employees.last_name,
#   products.product_name
# FROM employees
# JOIN orders ON employees.employee_id = orders.employee_id
# JOIN line_items ON orders.order_id = line_items.order_id
# JOIN products ON line_items.product_id = products.product_id
# LIMIT 5;
# '''

# cursor.execute(query)
# rows = cursor.fetchall()

# for employee_id, last_name, product_name in rows:
#     print(f'Employee {last_name} (ID: {employee_id}) sold {product_name} ')

# conn.close()

#Task2
# SELECT
# orders.customer_id AS customer_id_b,
# SUM (products.price * line_items.quantity) AS total_price
# FROM orders
# JOIN line_items on orders.id = line_items.order_id
# JOIN products ON line_items.products_id = products.product_id
# GROUP BY orders.id

# SELECT 
#   customers.customer_name,
#   AVG(order_totals.total_price) AS average_total_price
# FROM customers
# LEFT JOIN (
#   SELECT 
#     orders.customer_id AS customer_id_b,
#     SUM(products.price * line_items.quantity) AS total_price
#   FROM orders
#   JOIN line_items ON orders.id = line_items.order_id
#   JOIN products ON line_items.product_id = products.product_id
#   GROUP BY orders.id
# ) AS order_totals
# ON customers.customer_id = order_totals.customer_id_b
# GROUP BY customers.customer_id
# ORDER BY average_total_price DESC
# LIMIT 10;


# import sqlite3

# conn = sqlite3.connect("../db/lesson.db")
# cursor = conn.cursor()

# query = '''
# SELECT 
#   customers.customer_name,
#   AVG(order_totals.total_price) AS average_total_price
# FROM customers
# LEFT JOIN (
#   SELECT 
#     orders.customer_id AS customer_id_b,
#     SUM(products.price * line_items.quantity) AS total_price
#   FROM orders
#   JOIN line_items ON orders.order_id = line_items.order_id
#   JOIN products ON line_items.product_id = products.product_id
#   GROUP BY orders.order_id
# ) AS order_totals
# ON customers.customer_id = order_totals.customer_id_b
# GROUP BY customers.customer_id
# ORDER BY average_total_price DESC
# LIMIT 10;
# '''

# cursor.execute(query)
# rows = cursor.fetchall()

# for customer_name, avg_price in rows:
#     print(f'{customer_name}: Average Order Price = ${avg_price:.2f}')

#conn.close()

