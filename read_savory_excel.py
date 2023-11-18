import pandas as pd
import sqlite3

# เชื่อมต่อฐานข้อมูล SQLite3
database_path = 'database.db'
conn = sqlite3.connect(database_path)

# อ่านไฟล์ Excel
excel_file_path = 'savory.xlsx'
df = pd.read_excel(excel_file_path)

# แปลงชนิดข้อมูลในคอลัมน์ name ให้เป็น text
df['name'] = df['name'].astype(str)

# เช็คว่าคอลัมน์ 'id' มีใน DataFrame มั้ย
if 'id' not in df.columns:
    raise KeyError("The 'id' column is missing in the DataFrame.")

# สร้าง DataFrame ตามหัวข้อคอลัมน์ที่ต้องการ
selected_columns = ['id', 'name', 'kcal', 'protein', 'fat', 'carbohydrate', 'chili', 'rice', 'meat', 'shrimp-paste', 'noodle', 'soup', 'pickled-fish', 'one-dish-meal', 'fried', 'stir-fried']
df_selected = df[selected_columns]

# นำเข้าข้อมูลไปยังฐานข้อมูล SQLite
df_selected.to_sql('savory', conn, if_exists='replace', index=False)

# แสดงข้อความเมื่อนำเข้าสำเร็จ
print("Data imported successfully!")

# ปิดการเชื่อมต่อฐานข้อมูล SQLite
conn.close()