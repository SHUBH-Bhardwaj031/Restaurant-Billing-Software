
import sqlite3
from utils.db_utils import DB_PATH

def calculate_total(item_list, discount=0):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    total = 0
    detailed_items = []

    for item_name, qty in item_list:
        c.execute("SELECT price, gst FROM menu WHERE name=?", (item_name,))
        price, gst = c.fetchone()
        subtotal = (price * qty) * (1 + gst / 100)
        detailed_items.append({
            'name': item_name,
            'qty': qty,
            'price': price,
            'gst': gst,
            'subtotal': round(subtotal, 2)
        })
        total += subtotal

    if discount:
        total -= total * (discount / 100)

    conn.close()
    return detailed_items, round(total, 2)
