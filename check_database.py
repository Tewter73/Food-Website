import sqlite3

def display_table_data(table_name):
    conn = sqlite3.connect('database.db')  
    cursor = conn.cursor()

    # ดึงข้อมูลมาจากตารางใน database
    cursor.execute(f"SELECT * FROM {table_name};")
    table_data = cursor.fetchall()

    # แสดงผลลัพธ์เป็น List
    print(f"Data in table '{table_name}':")
    for row in table_data:
        print(row)

    # ปิดการเชื่อมต่อ
    conn.close()

if __name__ == '__main__':
    # เรียกดูข้อมูลอาหารคาว
    table_name = 'savory'
    display_table_data(table_name)
    # เรียกดูข้อมูลของหวาน
    table_name = 'dessert'
    display_table_data(table_name)