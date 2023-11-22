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
            style = f.read()
        st.markdown(f"<style>{style}</style>", unsafe_allow_html=True)

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

    def run(self):
        self.random_food_page()

    def random_food_page(self):
        st.markdown('<div class="subheader2">🔎 ระบบสุ่มอาหาร</div>', unsafe_allow_html=True)
        st.markdown('<div class="subheader3">💙 โปรดเลือกประเภทของเมนูอาหาร</div>', unsafe_allow_html=True)
        food_type = st.radio("| เลือกประเภทอาหาร :", ["อาหารประเภทของคาว", "อาหารประเภทของหวาน"])
        if food_type == "อาหารประเภทของคาว":
            if st.button("สุ่มเมนู"):
                self.show_random_food('savory')
        elif food_type == "อาหารประเภทของหวาน":
            if st.button("สุ่มเมนู"):
                self.show_random_food('dessert')
    
    def show_random_food(self, category):
        st.markdown('<div class="header">เมนูอาหารสำหรับคุณในมือนี้ ก็คือ !!!</div>', unsafe_allow_html=True)
        food_data = self.load_food_data_with_nutrition(category)
        if len(food_data) == 0:
            st.error("ไม่พบเมนูอาหารที่ท่านต้องการครับ")
        else:
            col1, col2, col3 = st.columns(3)
            random_food_indexes = random.sample(range(len(food_data)), min(3, len(food_data)))
            for index, food_index in enumerate(random_food_indexes):
                food_id, food_name, *_ = food_data[food_index]
                if index % 3 == 0:
                    with col1:
                        st.markdown(f'<div class="menu_topic">{food_name}</div>', unsafe_allow_html=True)
                        self.show_image_and_nutrition(food_id, food_name, category)

    def load_food_data_with_nutrition(self, category):
        return self.load_food_data(category)
    
    def load_food_data(self, category):
        self.database = Database('database.db')
        query = f"SELECT id, name, kcal, protein, fat, carbohydrate FROM {category};"
        return self.database.execute_query(query)
    
    def show_image_and_nutrition(self, food_id, food_name, category):
        image_path = f'images/{category}_images/{food_id}.jpg'

        try:
            img = self.resize_image(image_path)
            new_image = img.resize((2000, 1900))
            st.image(new_image, caption=None, use_column_width=False, width=300)
            
            food_data = self.load_food_data(category)
            for id, name, kcal, protein, fat, carbohydrate in food_data:
                if id == food_id:
                    self.show_nutrition_info(kcal, protein, fat, carbohydrate)
                    break

        except FileNotFoundError:
            st.warning(f'ไม่พบรูปภาพสำหรับ {food_name}')

    def resize_image(self, image_path, size=(1920, 1080)):
        original_image = Image.open(image_path)
        resized_image = original_image.resize(size)
        return resized_image
    
    def show_nutrition_info(self, kcal, protein, fat, carbohydrate):
        st.markdown(f'<div class="calorie">ปริมาณพลังงาน (kcal) : {kcal}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="protein">ปริมาณโปรตีน (g) : {protein}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="fat">ปริมาณไขมัน (g) : {fat}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="carbohydrate">ปริมาณคาร์โบไฮเดรต (g) : {carbohydrate}</div>', unsafe_allow_html=True)

streamlit_app = StreamlitApp()
streamlit_app.run()