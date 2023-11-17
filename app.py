import os
import streamlit as st
import sqlite3

def load_savory_foods():
    conn = sqlite3.connect('database.db')  # แทน 'your_database.db' ด้วยชื่อฐานข้อมูลของคุณ
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM อาหารคาว;")  # แทน 'อาหารคาว' ด้วยชื่อตารางของคุณ
    savory_foods = [(row[0], row[1]) for row in cursor.fetchall()]
    conn.close()
    return savory_foods

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

def show_savory_page():
    st.title('เมนูอาหารประเภทของคาว')
    savory_foods = load_savory_foods()
    for food_id, food_name in savory_foods:
        st.write(f"## {food_name}")
        image_path = f"images/savory/{food_id}.jpg"
        if os.path.isfile(image_path):
            st.image(image_path, caption=f"รูปภาพ {food_name}", use_column_width=True)
        else:
            st.warning("รูปภาพยังไม่มีในระบบ")

def show_sweet_page():
    st.title('เมนูอาหารประเภทของหวาน')
    # เพิ่มโค้ดเพื่อแสดงเมนูอาหารของหวานที่คุณต้องการ

if __name__ == '__main__':
    main()