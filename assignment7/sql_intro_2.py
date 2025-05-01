import pandas as pd
import sqlite3
import os

assignment_dir = os.path.dirname(os.path.abspath(__file__))
# db_path = os.path.join(assignment_dir, "db/lesson.db")
db_path = "/Users/OlegPavlyuk/python_class/python_homework/db/lesson.db"
output_path = os.path.join(assignment_dir, 'order_summary.csv')
try:
    # Connect to database
    conn = sqlite3.connect(db_path)
    
    # Verify connection success
    print("✅ Connected to database successfully.")

    # Create a cursor for executing queries
    cursor = conn.cursor()
    
    # Proceed with querying or data processing...
    
except sqlite3.Error as e:
    print(f"❌ Database error: {e}")

finally:
    if conn:
        conn.close()
        print("🔄 Connection closed.")
try:
    with sqlite3.connect(db_path) as conn:
        # Verify tables exist first
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [table[0] for table in cursor.fetchall()]

        
        if 'line_items' not in tables or 'products' not in tables: 
            raise ValueError("Required tables (line_items, products) not found in database")

		# Ensure tables contain data
        cursor.execute("SELECT COUNT(*) FROM line_items")
        line_items_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM products")
        products_count = cursor.fetchone()[0]

        if line_items_count == 0 or products_count == 0:
            raise ValueError("❌ Tables exist but contain no data. Insert sample data before proceeding.")	

        #  SQL statement to get line items with product info
        sql_statement = """
            SELECT 
                li.line_item_id,
                li.quantity,
                li.product_id,
                p.product_name,
                p.price
            FROM line_items li
            JOIN products p ON li.product_id = p.product_id
            LIMIT 5
        """

        df = pd.read_sql_query(sql_statement, conn)

        # Add the 'total' column (quantity × price)
        df['total'] = df['quantity'] * df['price']

        # Group by product_id and aggregate
        grouped_df = df.groupby('product_id').agg({
            'line_item_id': 'count',  # Count of line items per product
            'total': 'sum',           # Sum of totals per product
            'product_name': 'first'   # Get the product name (same for same product_id)
        }).reset_index()

        # Sort by product_name (alphabetical order)
        grouped_df = grouped_df.sort_values('product_name')

        # Rename columns for clarity
        grouped_df = grouped_df.rename(columns={
            'line_item_id': 'order_count',
            'total': 'total_revenue'
        })

        # Print the first 5 lines with a descriptive header
        print("\nFirst 5 Line Items with Product Information:")
        print("=" * 50)
        print(df.head())
        print(grouped_df.head())

        
        grouped_df.to_csv(output_path, index=False)
        print(f"\nSummary saved to: {output_path}")

except sqlite3.Error as e:
    print(f"Database error: {e}")

except Exception as e:
    print(f"Error: {e}")

			