# ทำการ Activate Python Virtual Environment ด้วยคำสั่ง env\Scripts\activate ก่อน
# pip freeze > requirements.txt เพื่อส่งไฟล์ให้คนอื่น
# pip install -r requirements.txt สำหรับการโหลด package ไปใช้
import streamlit as st
import sqlite3
from PIL import Image
import random

class Database:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def execute_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close_connection(self):
        self.conn.close()

class StreamlitApp:
    def __init__(self):
        self.food_app = FoodApp()
        self.database = Database('database.db')

    def local_css(self, file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    def run(self):
        st.set_page_config(
            page_title="วันนี้กินไรดี?",
            page_icon="🍔",
            layout="wide",
            initial_sidebar_state="expanded",
        )
        self.local_css("styles.css")
        self.food_app.run()

class FoodApp:
    def __init__(self):
        self.selected_page = None
        self.categories = ["หน้าหลัก", "เมนูอาหารทั้งหมด", "ค้นหาเมนูอาหารตามโภชนาการ", "สุ่มอาหาร"]
        self.database = Database('database.db')

    def run(self):
        self.selected_page = st.sidebar.selectbox("ไปยัง : ", self.categories)

        if self.selected_page == "หน้าหลัก":
            self.home_page()
        elif self.selected_page == "เมนูอาหารทั้งหมด":
            self.search_food_page()
        elif self.selected_page == "ค้นหาเมนูอาหารตามโภชนาการ":
            self.nutritional_food_page()
        elif self.selected_page == "สุ่มอาหาร":
            self.random_food_page()

    def load_food_data(self, category):
        query = f"SELECT id, name, kcal, protein, fat, carbohydrate FROM {category};"
        return self.database.execute_query(query)

    def load_food_data_with_nutrition(self, category):
        return self.load_food_data(category)
    
    def resize_image(self, image_path, size=(300, 300)):
        original_image = Image.open(image_path)
        resized_image = original_image.resize(size)
        return resized_image
    
    def show_nutrition_info(self, kcal, protein, fat, carbohydrate):
        st.write(f'**ปริมาณพลังงาน (kcal) :** {kcal}')
        st.write(f'**ปริมาณโปรตีน (g) :** {protein}')
        st.write(f'**ปริมาณไขมัน (g) :** {fat}')
        st.write(f'**ปริมาณคาร์โบไฮเดรต (g) :** {carbohydrate}')

    def show_image_and_nutrition(self, food_id, food_name, category):
        image_path = f'images/{category}_images/{food_id}.jpg'

        try:
            img = self.resize_image(image_path)
            st.image(img, caption=None, use_column_width=True, width=300)
            food_data = self.load_food_data(category)
            for id, name, kcal, protein, fat, carbohydrate in food_data:
                if id == food_id:
                    self.show_nutrition_info(kcal, protein, fat, carbohydrate)
                    break

        except FileNotFoundError:
            st.warning(f'ไม่พบรูปภาพสำหรับ {food_name}')

    def show_food_page(self, title, category):
        st.title(title)
        food_data = self.load_food_data_with_nutrition(category)

        col1, col2, col3 = st.columns(3)

        for index, (food_id, food_name, _, _, _, _) in enumerate(food_data):
            if index % 3 == 0:
                with col1:
                    st.write(food_name)
                    self.show_image_and_nutrition(food_id, food_name, category)
            elif index % 3 == 1:
                with col2:
                    st.write(food_name)
                    self.show_image_and_nutrition(food_id, food_name, category)
            else:
                with col3:
                    st.write(food_name)
                    self.show_image_and_nutrition(food_id, food_name, category)

    def show_savory_page(self):
        self.show_food_page('เมนูอาหารประเภทของคาว', 'savory')

    def show_dessert_page(self):
        self.show_food_page('เมนูอาหารประเภทของหวาน', 'dessert')

    def show_nutritional_food_page(self, category, kcal, protein, fat, carbohydrate):
        food_data = self.load_food_data(category)
        filtered_food_data = []
        for food_id, food_name, kcal_db, protein_db, fat_db, carbohydrate_db in food_data:
            if (
                (kcal is None or kcal_db >= kcal)
                and (protein is None or protein_db >= protein)
                and (fat is None or fat_db >= fat)
                and (carbohydrate is None or carbohydrate_db >= carbohydrate)
            ):
                filtered_food_data.append((food_id, food_name))

        if len(filtered_food_data) == 0:
            st.error("ไม่พบเมนูอาหารที่ท่านต้องการครับ")
        else:
            for food_id, food_name in filtered_food_data:
                st.write(food_name)
                self.show_image_and_nutrition(food_id, food_name, category)

    def show_random_food(self, category):
        st.title("เมนูอาหารสำหรับคุณในมือนี้ ก็คือ !!!")
        food_data = self.load_food_data_with_nutrition(category)
        random_food = random.choice(food_data)
        food_id, food_name, _, _, _, _ = random_food
        st.header((food_name))
        self.show_image_and_nutrition(food_id, food_name, category)

    def home_page(self):
        st.markdown('<div class="home">หน้าหลัก</div>', unsafe_allow_html=True)
        st.markdown('<div class="header">เกี่ยวกับเว็บไซต์ของเรา</div>', unsafe_allow_html=True)
        st.markdown('<div class="subheader">เหตุผลในการพัฒนา :</div>', unsafe_allow_html=True)
        st.markdown('<div class="passage">เคยมั้ยครับกับการที่เวลาเราเดินไปที่โรงอาหารแล้วเราไม่รู้จะสั่งเมนูอะไรดี สุดท้ายแล้วเราก็เลือกที่จะสั่งเมนูเดิม ๆ ซึ่งมันทำให้เปลืองเวลาค่อนข้างมากเลยใช่มั้ยล่ะครับ จุดประสงค์ของกลุ่มเราก็คือการมาแก้ปัญหาตรงนั้นครับ</div>', unsafe_allow_html=True)
        st.markdown('<div class="subheader">รายละเอียดเว็บไซต์</div>', unsafe_allow_html=True)
        st.markdown('<div class="passage">พวกเราได้สร้างเว็บไซต์สำหรับเลือกดูเมนูอาหาร โดยจะเน้นไปที่อาหารไทย ซึ่งเราก็จะสามารถหาดูอาหารพร้อมกับภาพประกอบ และข้อมูลโภชนาการให้เราได้เลือกรับประทานกันได้ง่าย ๆ ครับ</div>', unsafe_allow_html=True)
        st.markdown('<div class="subheader">สมาชิก</div>', unsafe_allow_html=True)
        st.markdown('<div class="passage">1. นายปภพ กิตติภิญโญชัย (6634438223)</div>', unsafe_allow_html=True)
        st.markdown('<div class="passage">2. นายคุณานนต์ โสภาเจริญ (6634406123)</div>', unsafe_allow_html=True)
        st.markdown('<div class="passage">3. นายกีรติ แก้วโนนตุ่น (6634405523)</div>', unsafe_allow_html=True)

    def search_food_page(self):
        st.title("โปรดเลือกประเภทของเมนูอาหาร")
        food_type = st.radio("เลือกประเภทอาหาร : ", ["อาหารประเภทของคาว", "อาหารประเภทของหวาน"])
        if food_type == "อาหารประเภทของคาว":
            if st.button("ยืนยัน"):
                self.show_savory_page()

        elif food_type == "อาหารประเภทของหวาน":
            if st.button("ยืนยัน"):
                self.show_dessert_page()

    def nutritional_food_page(self):
        st.title("โปรดเลือกประเภทของเมนูอาหาร")
        food_type = st.radio("เลือกประเภทอาหาร", ["อาหารประเภทของคาว", "อาหารประเภทของหวาน"])
        if food_type == "อาหารประเภทของคาว":
            category = "savory"
        elif food_type == "อาหารประเภทของหวาน":
            category = "dessert"

        kcal = st.number_input("ต้องการปริมาณพลังงานตั้งแต่ (kcal)", min_value=0)
        protein = st.number_input("ต้องการปริมาณโปรตีนตั้งแต่ (g)", min_value=0)
        fat = st.number_input("ต้องการปริมาณไขมันต้องตั้งแต่ (g)", min_value=0)
        carbohydrate = st.number_input("ต้องการปริมาณคาร์โบไฮเดรตต้องตั้งแต่ (g)", min_value=0)

        button = st.button("ค้นหา")

        if button:
            self.show_nutritional_food_page(category, kcal, protein, fat, carbohydrate)

    def random_food_page(self):
        st.title("สุ่มอาหาร")
        st.title("โปรดเลือกประเภทของเมนูอาหาร")
        food_type = st.radio("เลือกประเภทอาหาร", ["อาหารประเภทของคาว", "อาหารประเภทของหวาน"])
        if food_type == "อาหารประเภทของคาว":
            if st.button("สุ่มเมนู"):
                self.show_random_food('savory')
        elif food_type == "อาหารประเภทของหวาน":
            if st.button("สุ่มเมนู"):
                self.show_random_food('dessert')

streamlit_app = StreamlitApp()
streamlit_app.run()