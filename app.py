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
    cursor.execute("SELECT name FROM dessert;")  # 'sweet' คือชื่อตารางที่คุณสร้างจากไฟล์ Excel สำหรับข้อมูลเมนูหวาน
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

def main():
    st.title('วันนี้กินไรดี')
    st.subheader('เว็บไซต์สำหรับค้นหาอาหารไทยตามความต้องการของผู้ใช้งาน')
    st.subheader('โปรดเลือกประเภทอาหารที่ท่านสนใจ')

    # สร้างเลือกประเภทอาหาร
    food_type = st.radio("เลือกประเภทอาหาร", ["อาหารประเภทของคาว", "อาหารประเภทของหวาน"])

    # ตรวจสอบเงื่อนไขและแสดงข้อความที่เลือก
    if food_type == "อาหารประเภทของคาว":
        if st.button("ยืนยัน"):
            show_savory_page()

    elif food_type == "อาหารประเภทของหวาน":
        if st.button("ยืนยัน"):
            show_sweet_page()

def show_image(food_id, food_name, category):
    # โหลดรูปภาพจากโฟลเดอร์ images/category/
    image_path = f'images/{category}_images/{food_id}.jpg'
    
    try:
        img = Image.open(image_path)
        st.image(img, caption=f'รูปภาพของ {food_name}', use_column_width=True)
    except FileNotFoundError:
        st.warning(f'ไม่พบรูปภาพสำหรับ {food_name}')

def show_savory_page():
    st.title('เมนูอาหารประเภทของคาว')
    savory_data = load_food_data('savory')
    for food_id, food_name in savory_data:
        st.write(food_name)
        show_image(food_id, food_name, 'savory')

        # เพิ่มปุ่มดูรายละเอียดหรือคลิปเข้าไป
        if st.button(f'ข้อมูลเพิ่มเติมสำหรับ {food_name}'):
            # เพิ่มโค้ดที่ต้องการให้ทำงานเมื่อคลิกปุ่ม
            st.write(f'ข้อมูลโภชนาการของ {food_name}')

def show_sweet_page():
    st.title('เมนูอาหารประเภทของหวาน')
    sweet_data = load_food_data('dessert')
    for food_id, food_name in sweet_data:
        st.write(food_name)
        show_image(food_id, food_name, 'dessert')

        # เพิ่มปุ่มดูรายละเอียดหรือคลิปเข้าไป
        if st.button(f'ข้อมูลเพิ่มเติมสำหรับ {food_name}'):
            # เพิ่มโค้ดที่ต้องการให้ทำงานเมื่อคลิกปุ่ม
            st.write(f'ข้อมูลโภชนาการของ {food_name}')

if __name__ == '__main__':
    main()