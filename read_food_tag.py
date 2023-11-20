import sqlite3

def fetch_data_from_tables(database_file, savory_table_name, dessert_table_name, savory_columns, dessert_columns):
    # เชื่อมต่อกับฐานข้อมูล
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    # ทำคำสั่ง SQL เพื่อดึงข้อมูลจากตาราง savory
    savory_query = f"SELECT {', '.join(savory_columns)} FROM {savory_table_name}"
    cursor.execute(savory_query)
    savory_data = cursor.fetchall()

    # ทำคำสั่ง SQL เพื่อดึงข้อมูลจากตาราง dessert
    dessert_query = f"SELECT {', '.join(dessert_columns)} FROM {dessert_table_name}"
    cursor.execute(dessert_query)
    dessert_data = cursor.fetchall()

    # ปิด cursor และ connection
    cursor.close()
    connection.close()

    return savory_data, dessert_data

# กำหนดข้อมูลที่ต้องการดึงจากตาราง savory
savory_table_name = "savory"
savory_columns = ["chili", "rice", "meat", "shrimppaste", "noodle", "soup", "pickledfish", "onedishmeal", "fried", "stirfried"]

# กำหนดข้อมูลที่ต้องการดึงจากตาราง dessert
dessert_table_name = "dessert"
dessert_columns = ["water", "fruit", "cold", "hot", "thaidessert", "baked", "fried", "smallpiece"]

# เรียกใช้ฟังก์ชันเพื่อดึงข้อมูล
database_file = "database.db"
savory_data, dessert_data = fetch_data_from_tables(database_file, savory_table_name, dessert_table_name, savory_columns, dessert_columns)

# แสดงผลลัพธ์
print("Savory Data:")
for row in savory_data:
    print(row)

print("\nDessert Data:")
for row in dessert_data:
    print(row)