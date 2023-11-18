import sqlite3

# สร้างหรือเปิดฐานข้อมูล SQLite
database_path = 'database.db'
conn = sqlite3.connect(database_path)

# สร้าง cursor เพื่อทำการ execute SQL statements
cursor = conn.cursor()

# เพิ่มคอลัมน์ additional_info ในตาราง savory
cursor.execute("ALTER TABLE savory ADD COLUMN additional_info TEXT;")

# เพิ่มคอลัมน์ additional_info ในตาราง dessert
cursor.execute("ALTER TABLE dessert ADD COLUMN additional_info TEXT;")

# commit การเปลี่ยนแปลง
conn.commit()

# ปิดการเชื่อมต่อฐานข้อมูล SQLite
conn.close()