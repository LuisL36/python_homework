import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def main():
    conn = sqlite3.connect("../db/lesson.db")
    query = """
    SELECT last_name, SUM(price * quantity) AS revenue
    FROM employees e
    JOIN orders o ON e.employee_id = o.employee_id
    JOIN line_items l ON o.order_id = l.order_id
    JOIN products p ON l.product_id = p.product_id
    GROUP BY e.employee_id;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    df = df.sort_values(by="revenue", ascending=False).reset_index(drop=True)
    ax = df.plot(kind="bar", x="last_name", y="revenue", legend=False)
    ax.set_title("Revenue by Employee")
    ax.set_xlabel("Employee Last Name")
    ax.set_ylabel("Revenue (USD)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
