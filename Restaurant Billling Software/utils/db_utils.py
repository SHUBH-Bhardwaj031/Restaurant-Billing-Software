
import sqlite3
import os
import csv

DB_PATH = os.path.join("db", "restaurant.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT,
        price REAL,
        gst REAL
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_type TEXT,
        total_amount REAL,
        payment_method TEXT,
        timestamp TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        item_name TEXT,
        quantity INTEGER,
        price REAL,
        gst REAL,
        FOREIGN KEY(order_id) REFERENCES orders(order_id)
    )''')

    conn.commit()
    conn.close()

def insert_menu_from_csv(csv_path):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            c.execute("INSERT INTO menu (name, category, price, gst) VALUES (?, ?, ?, ?)", 
                      (row['name'], row['category'], float(row['price']), float(row['gst'])))
    conn.commit()
    conn.close()
