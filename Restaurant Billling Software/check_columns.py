import sqlite3

conn = sqlite3.connect('data/orders.db')
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(orders);")
columns = cursor.fetchall()

print("📋 Columns in 'orders' table:")
for col in columns:
    print(f"- {col[1]}")

conn.close()
