
from utils.db_utils import init_db, insert_menu_from_csv
import os

if __name__ == "__main__":
    init_db()
    print("Database Initialized ✅")

    menu_path = os.path.join("data", "menu.csv")
    insert_menu_from_csv(menu_path)
    print("Menu inserted from CSV ✅")
