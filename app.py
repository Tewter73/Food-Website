# ทำการ Activate Python Virtual Environment ด้วยคำสั่ง env\Scripts\activate ก่อน
# pip freeze > requirements.txt เพื่อส่งไฟล์ให้คนอื่นimport streamlit as st
import streamlit as st
import sqlite3
from PIL import Image
import random

st.set_page_config(
    page_title="วันนี้กินไรดี?",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.title("วันนี้กินไรดี")
st.sidebar.subheader("โปรดเลือก : ")

selected_page = st.sidebar.selectbox("ไปยัง", ["หน้าหลัก", "ค้นหาเมนูอาหารทั้งหมด", "เลือกอาหารตามความชอบ", "สุ่มอาหาร"])

def load_savory_foods():
    global conn, cursor
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM savory;")
    savory_foods = [row[0] for row in cursor.fetchall()]
    conn.close()
    return savory_foods

def load_dessert_foods():
    global conn, cursor
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM dessert;")
    dessert_foods = [row[0] for row in cursor.fetchall()]
    conn.close()
    return dessert_foods

def load_food_data_with_nutrition(category):
    global conn, cursor
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, name, kcal, protein, fat, carbohydrate FROM {category};")
    food_data = cursor.fetchall()
    conn.close()
    return food_data

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

    except FileNotFoundError:
        st.warning(f'ไม่พบรูปภาพสำหรับ {food_name}')

def show_savory_page():
    st.title('เมนูอาหารประเภทของคาว')
    savory_data = load_food_data_with_nutrition('savory')
    for food_id, food_name, kcal, protein, fat, carbohydrate in savory_data:
        st.write(food_name)
        show_image_and_nutrition(food_id, food_name, 'savory')

def show_dessert_page():
    st.title('เมนูอาหารประเภทของหวาน')
    sweet_data = load_food_data_with_nutrition('dessert')
    for food_id, food_name, kcal, protein, fat, carbohydrate in sweet_data:
        st.write(food_name)
        show_image_and_nutrition(food_id, food_name, 'dessert')

def show_random_food(category):
    st.title("เมนูอาหารสำหรับคุณในมือนี้ ก็คือ!!!")

    # โหลดข้อมูลอาหารจากฐานข้อมูล
    food_data = load_food_data_with_nutrition(category)

    # สุ่มเลือกเมนู
    random_food = random.choice(food_data)

    # แสดงข้อมูลเมนู
    food_id, food_name, _, _, _, _ = random_food
    st.header((food_name))

    # แสดงรูปภาพและข้อมูลโภชนาการ
    show_image_and_nutrition(food_id, food_name, category)

def home_page():
    st.title("หน้าหลัก")
    st.header("เกี่ยวกับเว็บไซต์ของเรา")
    st.subheader("เหตุผลในการพัฒนา :")
    st.write("เคยมั้ยครับกับการที่เวลาเราเดินไปที่โรงอาหารแล้วเราไม่รู้จะสั่งเมนูอะไรดี สุดท้ายแล้วเราก็เลือกที่จะสั่งเมนูเดิม ๆ ซึ่งมันทำให้เปลืองเวลาค่อนข้างมากเลยใช่มั้ยล่ะครับ จุดประสงค์ของกลุ่มเราก็คือการมาแก้ปัญหาตรงนั้นครับ")
    st.subheader("รายละเอียดเว็บไซต์")
    st.write("พวกเราได้สร้างเว็บไซต์สำหรับเลือกดูเมนูอาหาร โดยจะเน้นไปที่อาหารไทย ซึ่งเราก็จะสามารถหาดูอาหารพร้อมกับภาพประกอบ และข้อมูลโภชนาการให้เราได้เลือกรับประทานกันได้ง่าย ๆ ครับ")
    st.subheader("สมาชิก")
    st.write("1. นายปภพ กิตติภิญโญชัย (6634438223)")
    st.write("2. นายคุณานนต์ โสภาเจริญ (6634406123)")
    st.write("3. นายกีรติ แก้วโนนตุ่น (6634405523)")

def search_recipe_page():
    st.title("โปรดเลือกประเภทของเมนูอาหาร")
    food_type = st.radio("เลือกประเภทอาหาร", ["อาหารประเภทของคาว", "อาหารประเภทของหวาน"])
    if food_type == "อาหารประเภทของคาว":
        if st.button("ยืนยัน"):
            show_savory_page()

    elif food_type == "อาหารประเภทของหวาน":
        if st.button("ยืนยัน"):
            show_dessert_page()

def random_recipe_page():
    st.title("สุ่มอาหาร")
    st.title("โปรดเลือกประเภทของเมนูอาหาร")
    food_type = st.radio("เลือกประเภทอาหาร", ["อาหารประเภทของคาว", "อาหารประเภทของหวาน"])
    if food_type == "อาหารประเภทของคาว":
        if st.button("สุ่มเมนู"):
            show_random_food('savory')
    elif food_type == "อาหารประเภทของหวาน":
        if st.button("สุ่มเมนู"):
            show_random_food('dessert')

# แก้ไขเงื่อนไขเพื่อให้ search_and_tags ทำงานร่วมกับหน้าเว็บ
if selected_page == "หน้าหลัก":
    home_page()
elif selected_page == "ค้นหาเมนูอาหารทั้งหมด":
    search_recipe_page()
elif selected_page == "เลือกอาหารตามความชอบ":
    pass
elif selected_page == "สุ่มอาหาร":
    random_recipe_page()