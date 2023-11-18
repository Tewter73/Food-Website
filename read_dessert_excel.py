import pandas as pd
import sqlite3

# สร้างหรือเปิดฐานข้อมูล SQLite
database_path = 'database.db'
conn = sqlite3.connect(database_path)

# อ่านไฟล์ Excel
excel_file_path = 'dessert.xlsx'
df = pd.read_excel(excel_file_path)

# แปลงชนิดข้อมูลในคอลัมน์ name เป็น text
df['name'] = df['name'].astype(str)

# ตรวจสอบว่าคอลัมน์ 'id' มีอยู่ใน DataFrame หรือไม่
if 'id' not in df.columns:
    raise KeyError("The 'id' column is missing in the DataFrame.")

# สร้าง DataFrame ที่มีเฉพาะคอลัมน์ที่ต้องการ (รวมทั้ง 'id')
selected_columns = ['id', 'name', 'kcal', 'protein', 'fat', 'carbohydrate', 'water', 'fruit', 'cold', 'hot', 'thai-dessert', 'baked', 'fried', 'small-piece']
df_selected = df[selected_columns]

# นำเข้าข้อมูลไปยังฐานข้อมูล SQLite
df_selected.to_sql('dessert', conn, if_exists='replace', index=False)

# ปิดการเชื่อมต่อฐานข้อมูล SQLite
conn.close()

# แสดงข้อความเมื่อนำเข้าสำเร็จ
print("นำเข้าข้อมูลสำเร็จ!")

# ปิดการเชื่อมต่อฐานข้อมูล SQLite
conn.close()