import sqlite3

# เชื่อมต่อกับฐานข้อมูล SQLite
conn = sqlite3.connect('database.db')

# สร้าง Cursor object เพื่อทำการ query
cursor = conn.cursor()

# เรียกดูข้อมูลจากตาราง
cursor.execute("SELECT * FROM อาหารคาว;")
data = cursor.fetchall()

# แสดงข้อมูล
for row in data:
    print(row)

# ปิดการเชื่อมต่อ
conn.close()