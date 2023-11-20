import sqlite3

def get_table_headers(cursor, category):
    # สร้างคำสั่ง SQL สำหรับดึงรายละเอียดของตาราง
    pragma_query = f"PRAGMA table_info({category});"

    # ดึงข้อมูลจากฐานข้อมูล
    cursor.execute(pragma_query)
    headers_info = cursor.fetchall()

    # ดึงชื่อ column จากรายละเอียดของตาราง
    headers = [header_info[1] for header_info in headers_info]

    return headers

def read_table_data(category):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # ดึงชื่อ header จากฐานข้อมูล
    headers = get_table_headers(cursor, category)

    # สร้างคำสั่ง SQL สำหรับเลือกข้อมูล
    select_query = f"SELECT * FROM {category};"

    # ดึงข้อมูลจากฐานข้อมูล
    cursor.execute(select_query)
    rows = cursor.fetchall()

    # ปิดการเชื่อมต่อ
    conn.close()

    # สร้างลิสต์ของดิกชันนารีส์
    data = []
    for row in rows:
        row_dict = dict(zip(headers, row))
        data.append(row_dict)

    return data

# ตัวอย่างการใช้งาน
savory_data = read_table_data('savory')
dessert_data = read_table_data('dessert')

# แสดงผลลัพธ์
print("Savory Data:")
for row in savory_data:
    print(row)

print("\nDessert Data:")
for row in dessert_data:
    print(row)