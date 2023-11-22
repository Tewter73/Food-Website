import pandas as pd
import sqlite3

database_path = 'database.db'
conn = sqlite3.connect(database_path)

excel_file_path = 'dessert.xlsx'
df = pd.read_excel(excel_file_path)

df['name'] = df['name'].astype(str)

if 'id' not in df.columns:
    raise KeyError("The 'id' column is missing in the DataFrame.")

selected_columns = ['id', 'name', 'kcal', 'protein', 'fat', 'carbohydrate']
df_selected = df[selected_columns]

df_selected.to_sql('dessert', conn, if_exists='replace', index=False)

print("Data imported successfully!")

conn.close()