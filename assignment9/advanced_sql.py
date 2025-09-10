import sqlite3

conn = sqlite3.connect("../db/lesson.db")
conn.execute("PRAGMA foreign_keys = 1")
cursor = conn.cursor()


# Task 1: Complex JOINs with Aggregation

print("Task 1: Total price of first 5 orders")
cursor.execute("""
    SELECT o.order_id, SUM(p.price * li.quantity) AS total_price
    FROM orders o
    JOIN line_items li ON o.order_id = li.order_id
    JOIN products p ON li.product_id = p.product_id
    GROUP BY o.order_id
    ORDER BY o.order_id
    LIMIT 5;
""")
for row in cursor.fetchall():
    print(row)


# Task 2: Understanding Subqueries

print("\nTask 2: Average price of orders per customer")
cursor.execute("""
    SELECT c.customer_name, AVG(order_totals.total_price) AS average_total_price
    FROM customers c
    LEFT JOIN (
        SELECT o.customer_id AS customer_id_b,
               SUM(p.price * li.quantity) AS total_price
        FROM orders o
        JOIN line_items li ON o.order_id = li.order_id
        JOIN products p ON li.product_id = p.product_id
        GROUP BY o.order_id
    ) AS order_totals
    ON c.customer_id = order_totals.customer_id_b
    GROUP BY c.customer_id;
""")
for row in cursor.fetchall():
    print(row)


# Task 3: Insert Transaction Based on Data

print("\nTask 3: Create new order for Perez and Sons")
try:
    # Start a transaction
    conn.execute("BEGIN;")

   
    customer_id = 16  # Perez and Sons
    employee_id = 7   # Miranda Harris
    product_ids = [23, 18, 43, 9, 44]  # 5 cheapest products

    # Insert order
    cursor.execute("""
        INSERT INTO orders (customer_id, employee_id, date)
        VALUES (?, ?, DATE('now'))
    """, (customer_id, employee_id))
    order_id = cursor.lastrowid

    # Insert line items
    for pid in product_ids:
        cursor.execute("""
            INSERT INTO line_items (order_id, product_id, quantity)
            VALUES (?, ?, 10)
        """, (order_id, pid))

    # Commit transaction
    conn.commit()

    # Verify inserted line items
    cursor.execute("""
        SELECT li.line_item_id, li.quantity, p.product_name
        FROM line_items li
        JOIN products p ON li.product_id = p.product_id
        WHERE li.order_id = ?;
    """, (order_id,))
    for row in cursor.fetchall():
        print(row)

except Exception as e:
    print("Error:", e)
    conn.rollback()


# Task 4: Aggregation with HAVING

print("\nTask 4: Employees with more than 5 orders")
cursor.execute("""
    SELECT e.employee_id, e.first_name, e.last_name, COUNT(o.order_id) AS order_count
    FROM employees e
    JOIN orders o ON e.employee_id = o.employee_id
    GROUP BY e.employee_id
    HAVING COUNT(o.order_id) > 5;
""")
for row in cursor.fetchall():
    print(row)


conn.close()
