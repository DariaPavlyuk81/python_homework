#Task3
# import sqlite3
# conn = sqlite3.connect("../db/lesson.db")
# conn.execute("PRAGMA foreign_keys = 1")
# cursor = conn.cursor()

# try:
#     #start transaction
#     conn.execute("BEGIN")

#     #get customer_id for 'Perez and Sons'
#     cursor.execute("SELECT customer_id FROM customers WHERE customer_name = 'Perez and Sons'")
#     customer_id = cursor.fetchone()[0]

#     #get employee_id 'Miranda Harris'
#     cursor.execute("SELECT employee_id FROM employees WHERE first_name = 'Miranda' AND last_name = 'Harris'")
#     employee_id = cursor.fetchone()[0]

#     #get the 5 least expensive products
#     cursor.execute("SELECT product_id FROM products ORDER BY price ASC LIMIT 5")
#     product_ids = [row[0] for row in cursor.fetchall()]

#     #insertorder and get its order_id
#     cursor.execute("INSERT INTO orders (customer_id, employee_id) VALUES (?, ?) RETURNING order_id",(customer_id, employee_id)
#     )
#     order_id = cursor.fetchone()[0]

#     #insert 5 lineitems with quantity10
#     for product_id in product_ids:
#         cursor.execute(
#             "INSERT INTO line_items (order_id, product_id, quantity) VALUES (?, ?, ?)", (order_id, product_id, 10)
#         )

#     conn.commit()

#     # Select and display line_item details
#     cursor.execute("""
#     SELECT 
#         line_items.line_item_id,
#         line_items.quantity,
#         products.product_name
#     FROM line_items
#     JOIN products ON line_items.product_id = products.product_id
#     WHERE line_items.order_id = ?
#     """, (order_id,))

#     rows = cursor.fetchall()
#     print(f"Line items for new order (order_id = {order_id}):")
#     for line_item_id, quantity, product_name in rows:
#         print(f"Line Item ID: {line_item_id}, Quantity: {quantity}, Product: {product_name}")

# except Exception as e:
#     print("Transaction failed:", e)
#     conn.rollback()

# finally:
#     conn.close()

    #TASK4
# SELECT 
#   employees.employee_id,
#   employees.first_name,
#   employees.last_name,
#   COUNT(orders.order_id) AS order_count
# FROM employees
# JOIN orders ON employees.employee_id = orders.employee_id
# GROUP BY employees.employee_id
# HAVING COUNT(orders.order_id) > 5;

import sqlite3

# Connect to database
conn = sqlite3.connect("../db/lesson.db")
conn.execute("PRAGMA foreign_keys = 1")
cursor = conn.cursor()

# find employees with more than 5 orders
query = '''
SELECT 
  employees.employee_id,
  employees.first_name,
  employees.last_name,
  COUNT(orders.order_id) AS order_count
FROM employees
JOIN orders ON employees.employee_id = orders.employee_id
GROUP BY employees.employee_id
HAVING COUNT(orders.order_id) > 5;
'''

cursor.execute(query)
rows = cursor.fetchall()

# Print the results
print("Employees with more than 5 orders:\n")
for emp_id, first_name, last_name, count in rows:
    print(f"{emp_id}: {first_name} {last_name} - {count} orders")

conn.close()
