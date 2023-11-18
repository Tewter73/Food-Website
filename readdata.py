import sqlite3

def read_table_data(category):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # กำหนดหัวข้อที่ต้องการอ่าน โดยอิงจาก category
    if category == 'savory':
        headers = ["chili", "rice", "meat", "shrimp-paste", "noodle", "soup", "pickled_fish", "one_dish_meal", "fried", "stir_fried"]
    elif category == 'dessert':
        headers = ["water", "fruit", "cold", "hot", "thai-dessert", "baked", "fried", "small-piece"]
    else:
        print("Invalid category")
        return

    # สร้างคำสั่ง SQL สำหรับเลือกข้อมูล
    select_query = f"SELECT {', '.join(headers)} FROM {category};"

    # ดึงข้อมูลจากฐานข้อมูล
    cursor.execute(select_query)
    data = cursor.fetchall()

    # ปิดการเชื่อมต่อ
    conn.close()

    return data

# ตัวอย่างการใช้งาน
savory_data = read_table_data('savory')
dessert_data = read_table_data('dessert')

print("Savory Data:")
print(savory_data)

print("\nDessert Data:")
print(dessert_data)