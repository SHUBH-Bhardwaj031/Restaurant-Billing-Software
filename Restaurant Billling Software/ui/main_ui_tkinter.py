import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import sqlite3
from datetime import datetime

# Connect to database
conn = sqlite3.connect('db/restaurant.db')
cursor = conn.cursor()

# Load menu from CSV
menu_df = pd.read_csv('data/menu.csv')

# Setup GUI
root = tk.Tk()
root.title("Restaurant Billing System")
root.geometry("800x600")

# Order list
order = []

def add_to_order():
    item = item_combo.get()
    qty = qty_var.get()
    if not item or qty <= 0:
        messagebox.showerror("Error", "Please select an item and quantity > 0")
        return

    selected = menu_df[menu_df['item'] == item].iloc[0]
    price = selected['price']
    gst = selected['gst']
    order.append({
        "item": item,
        "qty": qty,
        "price": price,
        "gst": gst
    })
    update_order_table()

def update_order_table():
    for i in tree.get_children():
        tree.delete(i)
    for row in order:
        total = row['qty'] * row['price']
        tree.insert('', tk.END, values=(row['item'], row['qty'], row['price'], total))

def calculate_total():
    subtotal = sum(row['qty'] * row['price'] for row in order)
    gst_amount = sum((row['price'] * row['gst'] / 100) * row['qty'] for row in order)
    return subtotal + gst_amount

def submit_order():
    if not order:
        messagebox.showerror("Error", "No items in order.")
        return

    mode = mode_var.get()
    payment = payment_var.get()
    total_amount = calculate_total()
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insert into orders
    cursor.execute("INSERT INTO orders (mode, payment, total, datetime) VALUES (?, ?, ?, ?)",
                   (mode, payment, total_amount, dt))
    order_id = cursor.lastrowid

    # Insert order items
    for row in order:
        cursor.execute("INSERT INTO order_items (order_id, item, qty, price, gst) VALUES (?, ?, ?, ?, ?)",
                       (order_id, row['item'], row['qty'], row['price'], row['gst']))

    conn.commit()
    messagebox.showinfo("Success", f"Order #{order_id} placed successfully!")
    order.clear()
    update_order_table()

# Dropdowns and Inputs
item_combo = ttk.Combobox(root, values=menu_df['name'].tolist())
item_combo.grid(row=0, column=0, padx=10, pady=10)
item_combo.set("Select item")

qty_var = tk.IntVar(value=1)
qty_entry = tk.Entry(root, textvariable=qty_var)
qty_entry.grid(row=0, column=1, padx=10)

add_btn = tk.Button(root, text="Add to Order", command=add_to_order)
add_btn.grid(row=0, column=2, padx=10)

# Order table
columns = ("Item", "Qty", "Price", "Total")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

# Mode & Payment Dropdowns
mode_var = tk.StringVar(value="Dine-In")
payment_var = tk.StringVar(value="Cash")

ttk.Label(root, text="Mode:").grid(row=2, column=0, sticky='e')
ttk.Combobox(root, textvariable=mode_var, values=["Dine-In", "Takeaway"]).grid(row=2, column=1)

ttk.Label(root, text="Payment:").grid(row=3, column=0, sticky='e')
ttk.Combobox(root, textvariable=payment_var, values=["Cash", "Card", "UPI"]).grid(row=3, column=1)

submit_btn = tk.Button(root, text="Submit Order", command=submit_order)
submit_btn.grid(row=4, column=1, pady=20)

root.mainloop()
