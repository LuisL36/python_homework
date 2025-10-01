import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def main():
    conn = sqlite3.connect("../db/lesson.db")
    query = """
    SELECT o.order_id, SUM(p.price * l.quantity) AS total_price
    FROM orders o
    JOIN line_items l ON o.order_id = l.order_id
    JOIN products p ON l.product_id = p.product_id
    GROUP BY o.order_id
    ORDER BY o.order_id;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    df = df.sort_values("order_id").reset_index(drop=True)
    df["total_price"] = pd.to_numeric(df["total_price"], errors="coerce").fillna(0.0)
    df["cumulative"] = df["total_price"].cumsum()
    ax = df.plot(x="order_id", y="cumulative", kind="line", marker="o")
    ax.set_title("Cumulative Revenue Over Orders")
    ax.set_xlabel("Order ID")
    ax.set_ylabel("Cumulative Revenue (USD)")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
