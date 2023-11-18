# ทำการ Activate Python Virtual Environment ด้วยคำสั่ง env\Scripts\activate ก่อน
import streamlit as st
import sqlite3
from PIL import Image
import io

def load_savory_foods():
    conn = sqlite3.connect('database.db')  
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM savory;")  
    savory_foods = [row[0] for row in cursor.fetchall()]
    conn.close()
    return savory_foods

def load_sweet_foods():
    conn = sqlite3.connect('database.db')  
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM dessert;")  
    sweet_foods = [row[0] for row in cursor.fetchall()]
    conn.close()
    return sweet_foods

def load_food_data(category):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, name FROM {category};")
    food_data = cursor.fetchall()
    conn.close()
    return food_data

def load_food_data_with_nutrition(category):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, name, kcal, protein, fat, carbohydrate FROM {category};")
    food_data = cursor.fetchall()
    conn.close()
    return food_data

def get_additional_info(food_id, category):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT additional_info FROM {category} WHERE id = ?;", (food_id,))
    additional_info = cursor.fetchone()[0]
    conn.close()
    return additional_info

def main():
    st.title('วันนี้กินไรดี')
    st.subheader('เว็บไซต์สำหรับค้นหาอาหารไทยตามความต้องการของผู้ใช้งาน')
    st.subheader('โปรดเลือกประเภทอาหารที่ท่านสนใจ')

    # สร้างเลือกประเภทอาหาร
    food_type = st.radio("เลือกประเภทอาหาร", ["อาหารประเภทของคาว", "อาหารประเภทของหวาน"])

    # ตรวจสอบเงื่อนไขและแสดงข้อความที่เลือก
    if food_type == "อาหารประเภทของคาว":
        show_savory_page()

    elif food_type == "อาหารประเภทของหวาน":
        show_sweet_page()

def show_image_and_nutrition(food_id, food_name, category):
    # โหลดรูปภาพจากโฟลเดอร์ images/category/
    image_path = f'images/{category}_images/{food_id}.jpg'
    
    try:
        img = Image.open(image_path)
        st.image(img, caption=f'รูปภาพของ {food_name}', use_column_width=True)

        # แสดงข้อมูลโภชนาการ
        food_data = load_food_data_with_nutrition(category)
        for id, name, kcal, protein, fat, carbohydrate in food_data:
            if id == food_id:
                st.write(f'**ปริมาณพลังงาน (kcal):** {kcal}')
                st.write(f'**ปริมาณโปรตีน (g):** {protein}')
                st.write(f'**ปริมาณไขมัน (g):** {fat}')
                st.write(f'**ปริมาณคาร์โบไฮเดรต (g):** {carbohydrate}')
                break

        # แสดงข้อมูลเพิ่มเติมจากฐานข้อมูล
        additional_info = get_additional_info(food_id, category)
        st.write('**ข้อมูลเพิ่มเติม:**')
        st.write(additional_info)

    except FileNotFoundError:
        st.warning(f'ไม่พบรูปภาพสำหรับ {food_name}')

def show_savory_page():
    st.title('เมนูอาหารประเภทของคาว')
    savory_data = load_food_data_with_nutrition('savory')
    for food_id, food_name, kcal, protein, fat, carbohydrate in savory_data:
        st.write(food_name)
        show_image_and_nutrition(food_id, food_name, 'savory')

def show_sweet_page():
    st.title('เมนูอาหารประเภทของหวาน')
    sweet_data = load_food_data_with_nutrition('dessert')
    for food_id, food_name, kcal, protein, fat, carbohydrate in sweet_data:
        st.write(food_name)
        show_image_and_nutrition(food_id, food_name, 'dessert')

if __name__ == '__main__':
    main()