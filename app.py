import streamlit as st
import sqlite3

def load_savory_foods():
    conn = sqlite3.connect('database.db')  
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM อาหารคาว;")  
    savory_foods = [row[0] for row in cursor.fetchall()]
    conn.close()
    return savory_foods

def load_sweet_foods():
    conn = sqlite3.connect('database.db')  
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sweet;")  # 'sweet' คือชื่อตารางที่คุณสร้างจากไฟล์ Excel สำหรับข้อมูลเมนูหวาน
    sweet_foods = [row[0] for row in cursor.fetchall()]
    conn.close()
    return sweet_foods

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
    for food in savory_foods:
        st.write(food)

def show_sweet_page():
    st.title('เมนูอาหารประเภทของหวาน')
    sweet_foods = load_sweet_foods()
    for food in sweet_foods:
        st.write(food)

if __name__ == '__main__':
    main()