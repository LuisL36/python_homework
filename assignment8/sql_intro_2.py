import sqlite3
import pandas as pd

def main():
    try:
        conn = sqlite3.connect("../db/lesson.db")

        query = """
            SELECT 
                line_items.line_item_id,
                line_items.quantity,
                products.product_id,
                products.product_name,
                products.price
            FROM line_items
            JOIN products ON line_items.product_id = products.product_id
        """

        df = pd.read_sql_query(query, conn)
        print("\nFirst 5 rows of DataFrame:")
        print(df.head())

        # Add total column
        df['total'] = df['quantity'] * df['price']
        print("\nWith total column:")
        print(df.head())

        # Group by product
        summary = df.groupby('product_id').agg({
            'line_item_id': 'count',
            'total': 'sum',
            'product_name': 'first'
        }).reset_index()

        # Sort by product name
        summary = summary.sort_values(by='product_name')

        print("\nOrder Summary:")
        print(summary.head())

        # Save to CSV
        summary.to_csv("order_summary.csv", index=False)
        print("\norder_summary.csv created successfully")

    except sqlite3.Error as e:
        print("SQL Error:", e)

if __name__ == "__main__":
    main()
