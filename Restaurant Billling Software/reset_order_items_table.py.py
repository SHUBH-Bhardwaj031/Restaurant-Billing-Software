# reset_orders_and_items.py

import sqlite3

conn = sqlite3.connect('db/restaurant.db')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS orders")
cursor.execute("DROP TABLE IF EXISTS order_items")

cursor.execute('''
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mode TEXT,
    payment TEXT,
    total REAL,
    datetime TEXT
)
''')

cursor.execute('''
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    item TEXT,
    qty INTEGER,
    price REAL,
    gst REAL,
    FOREIGN KEY(order_id) REFERENCES orders(id)
)
''')

conn.commit()
conn.close()

print("✅ Tables reset successfully.")
