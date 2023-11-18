import sqlite3

def display_table_data(table_name):
    conn = sqlite3.connect('database.db')  
    cursor = conn.cursor()

    # ดึงข้อมูลจากตาราง
    cursor.execute(f"SELECT * FROM {table_name};")
    table_data = cursor.fetchall()

    # แสดงผลลัพธ์เป็น list
    print(f"Data in table '{table_name}':")
    for row in table_data:
        print(row)

    # ปิดการเชื่อมต่อ
    conn.close()

if __name__ == '__main__':
    table_name = 'Savory'  # แทนที่ด้วยชื่อตารางที่คุณต้องการดูข้อมูล
    display_table_data(table_name)
    table_name = 'Dessert'
    display_table_data(table_name)