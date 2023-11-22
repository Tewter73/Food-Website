import sqlite3

def display_table_data(table_name):
    conn = sqlite3.connect('database.db')  
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table_name};")
    table_data = cursor.fetchall()

    print(f"Data in table '{table_name}':")
    for row in table_data:
        print(row)

    conn.close()

if __name__ == '__main__':
    table_name = 'savory'
    display_table_data(table_name)
    table_name = 'dessert'
    display_table_data(table_name)