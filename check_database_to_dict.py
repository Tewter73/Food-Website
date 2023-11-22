import sqlite3

def get_table_headers(cursor, category):
    pragma_query = f"PRAGMA table_info({category});"
    cursor.execute(pragma_query)
    headers_info = cursor.fetchall()
    headers = [header_info[1] for header_info in headers_info]
    return headers

def read_table_data(category):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    headers = get_table_headers(cursor, category)
    select_query = f"SELECT * FROM {category};"
    cursor.execute(select_query)
    rows = cursor.fetchall()
    conn.close()
    data = []
    for row in rows:
        row_dict = dict(zip(headers, row))
        data.append(row_dict)
    return data

savory_data = read_table_data('savory')
dessert_data = read_table_data('dessert')

print("Savory Data:")
for row in savory_data:
    print(row)

print("\nDessert Data:")
for row in dessert_data:
    print(row)