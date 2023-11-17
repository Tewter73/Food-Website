import pandas as pd
import sqlite3

# แทนที่ 'your_file.xlsx' ด้วยชื่อไฟล์ Excel ของคุณ
df = pd.read_excel('อาหารคาว.xlsx')


# แทนที่ 'your_database.db' ด้วยชื่อฐานข้อมูล SQLite ของคุณ
conn = sqlite3.connect('database.db')

# แทนที่ 'your_table' ด้วยชื่อตารางที่คุณต้องการ
df.to_sql('อาหารคาว', conn, index=False, if_exists='replace')

conn.close()