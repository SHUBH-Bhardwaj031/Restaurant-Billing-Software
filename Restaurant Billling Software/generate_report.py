
import sqlite3
import pandas as pd
from utils.db_utils import DB_PATH

def generate_report():
    conn = sqlite3.connect(DB_PATH)

    orders = pd.read_sql_query("SELECT * FROM orders", conn)
    items = pd.read_sql_query("SELECT * FROM order_items", conn)

    orders['date'] = pd.to_datetime(orders['timestamp']).dt.date
    daily_sales = orders.groupby('date')['total_amount'].sum().reset_index()
    top_items = items.groupby('item_name')['quantity'].sum().sort_values(ascending=False).reset_index()

    daily_sales.to_csv("data/sales_report.csv", index=False)
    top_items.to_csv("data/top_items.csv", index=False)

    print("✅ Reports generated: sales_report.csv & top_items.csv")

if __name__ == "__main__":
    generate_report()
