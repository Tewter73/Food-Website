import pandas as pd
import sqlite3

# อ่านข้อมูลจากไฟล์ Excel
excel_file = 'dessert.xlsx'  # แทนที่ path/to/your/excel/file.xlsx ด้วยที่อยู่ของไฟล์ Excel ของคุณ
df = pd.read_excel(excel_file)

# สร้างฐานข้อมูล SQLite
conn = sqlite3.connect('database.db')  # แทน 'database.db' ด้วยชื่อฐานข้อมูลของคุณ

# เขียนข้อมูลไปยังตารางใหม่
table_name = 'dessert'  # ตั้งชื่อตารางใหม่ที่คุณต้องการ
df.to_sql(table_name, conn, index=False, if_exists='replace')  # 'replace' จะแทนที่ตารางที่มีอยู่ (ถ้ามี)

print(f'Table {table_name} created successfully.')

# ปิดการเชื่อมต่อ
conn.close()