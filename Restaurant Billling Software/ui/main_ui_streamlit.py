import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Database connection
conn = sqlite3.connect('db/restaurant.db', check_same_thread=False)
cursor = conn.cursor()

# Sidebar - Upload Menu
st.sidebar.header("📥 Upload Menu CSV")
menu_file = st.sidebar.file_uploader("Upload menu.csv", type=["csv"])

if menu_file:
    menu_df = pd.read_csv(menu_file)
    menu_df.columns = menu_df.columns.str.lower()
    st.write("Columns:", menu_df.columns.tolist())
    st.session_state['menu'] = menu_df
    st.success("Menu uploaded successfully!")

# Main UI
st.title("🍽️ Restaurant Billing System")

if 'menu' in st.session_state:
    menu_df = st.session_state['menu']
    
    # Order Mode
    mode = st.radio("Select Mode", ["Dine-In", "Takeaway"])
    
    # Select Item and Quantity
    item = st.selectbox("Select Item", menu_df['name'])  

    quantity = st.number_input("Quantity", min_value=1, step=1)
    if st.button("Add to Order"):
        if 'order' not in st.session_state:
            st.session_state['order'] = []
        selected = menu_df[menu_df['name'] == item].iloc[0]  # ✅ ab koi error nahi aayega

        st.session_state['order'].append({
            'item': item,
            'qty': quantity,
            'price': selected['price'],
            'gst': selected['gst']
        })
    
    # Show Running Order
    if 'order' in st.session_state and st.session_state['order']:
        st.subheader("🧾 Current Order")
        df = pd.DataFrame(st.session_state['order'])
        df['subtotal'] = df['qty'] * df['price']
        df['gst_amt'] = df['subtotal'] * df['gst'] / 100
        df['total'] = df['subtotal'] + df['gst_amt']
        st.dataframe(df[['item', 'qty', 'price', 'subtotal', 'gst_amt', 'total']])
        
        total_amount = df['total'].sum()
        st.write(f"### 💰 Grand Total: ₹{total_amount:.2f}")
        
        # Payment Method
        payment = st.radio("Payment Method", ["Cash", "Card", "UPI"])
        
        # Finalize Bill
        if st.button("Generate Bill"):
            dt = datetime.now()
            cursor.execute("INSERT INTO orders (mode, payment, total, datetime) VALUES (?, ?, ?, ?)",
                           (mode, payment, total_amount, dt))
            order_id = cursor.lastrowid
            for row in st.session_state['order']:
                cursor.execute("INSERT INTO order_items (order_id, item, qty, price, gst) VALUES (?, ?, ?, ?, ?)",
                               (order_id, row['item'], row['qty'], row['price'], row['gst']))
            conn.commit()
            st.success("✅ Bill Generated & Saved")
            st.session_state.pop('order')  # clear order after billing
    else:
        st.info("🛒 Add items to order first.")
else:
    st.warning("⚠️ Please upload a valid menu.csv file from sidebar.")
