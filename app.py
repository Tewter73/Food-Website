# ทำการ Activate Python Virtual Environment ด้วยคำสั่ง env\Scripts\activate ก่อน
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
    def __init__(self):
        self.selected_page = None
        self.categories = ["🏠 หน้าหลัก", "🔎 ค้นหาเมนูอาหารทั้งหมด", "🥗 ค้นหาเมนูอาหารตามโภชนาการ", "🎲 ระบบสุ่มอาหาร"]
        self.database = Database('database.db')
    
    def run(self):
        self.selected_page = st.sidebar.selectbox("ไปยัง : ", self.categories)

        if self.selected_page == "🏠 หน้าหลัก":
            self.home_page()
        elif self.selected_page == "🔎 ค้นหาเมนูอาหารทั้งหมด":
            self.search_food_page()
        elif self.selected_page == "🥗 ค้นหาเมนูอาหารตามโภชนาการ":
            self.nutritional_food_page()
        elif self.selected_page == "🎲 ระบบสุ่มอาหาร":
            self.random_food_page()

    def load_food_data(self, category):
        query = f"SELECT id, name, kcal, protein, fat, carbohydrate FROM {category};"
        return self.database.execute_query(query)
    
    def load_food_data_with_nutrition(self, category):
        return self.load_food_data(category)
    
    def resize_image(self, image_path, size=(1920, 1080)):
        original_image = Image.open(image_path)
        resized_image = original_image.resize(size)
        return resized_image
    
    def show_nutrition_info(self, kcal, protein, fat, carbohydrate):
        st.markdown(f'<div class="calorie">ปริมาณพลังงาน (kcal) : {kcal}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="protein">ปริมาณโปรตีน (g) : {protein}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="fat">ปริมาณไขมัน (g) : {fat}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="carbohydrate">ปริมาณคาร์โบไฮเดรต (g) : {carbohydrate}</div>', unsafe_allow_html=True)

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

    def show_food_page(self, title, category):
        st.markdown(f'<div class="subheader">| {title}</div>', unsafe_allow_html=True)
        food_data = self.load_food_data_with_nutrition(category)

        col1, col2, col3 = st.columns(3)

        for index, (food_id, food_name, _, _, _, _) in enumerate(food_data):
            if index % 3 == 0:
                with col1:
                    st.markdown(f'<div class="menu_topic">{food_name}</div>', unsafe_allow_html=True)
                    self.show_image_and_nutrition(food_id, food_name, category)
            elif index % 3 == 1:
                with col2:
                    st.markdown(f'<div class="menu_topic">{food_name}</div>', unsafe_allow_html=True)
                    self.show_image_and_nutrition(food_id, food_name, category)
            else:
                with col3:
                    st.markdown(f'<div class="menu_topic">{food_name}</div>', unsafe_allow_html=True)
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
            col1, col2, col3 = st.columns(3)

            for index, (food_id, food_name) in enumerate(filtered_food_data):
                if index % 3 == 0:
                    with col1:
                        st.markdown(f'<div class="menu_topic">{food_name}</div>', unsafe_allow_html=True)
                        self.show_image_and_nutrition(food_id, food_name, category)
                elif index % 3 == 1:
                    with col2:
                        st.markdown(f'<div class="menu_topic">{food_name}</div>', unsafe_allow_html=True)
                        self.show_image_and_nutrition(food_id, food_name, category)
                else:
                    with col3:
                        st.markdown(f'<div class="menu_topic">{food_name}</div>', unsafe_allow_html=True)
                        self.show_image_and_nutrition(food_id, food_name, category)

    def show_random_food(self, category):
        st.markdown('<div class="header">เมนูอาหารสำหรับคุณในมื้อนี้ ก็คือ !!!</div>', unsafe_allow_html=True)
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

    def home_page(self):
        st.markdown('<div class="home">🏠 หน้าหลัก</div>', unsafe_allow_html=True)
        st.markdown('<div class="header">🍔 เกี่ยวกับเว็บไซต์ของเรา</div>', unsafe_allow_html=True)
        st.markdown('<div class="subheader">| เหตุผลในการพัฒนา</div>', unsafe_allow_html=True)
        st.markdown('<div class="passage">บางครั้งเมื่อเราออกกำลังกาย และต้องการอยากที่จะคุมอาหารเพื่อสุขภาพที่ดี เราต้องการที่จะทราบถึงปริมาณสารอาหารที่เหมาะสมกับตัวเรา แล้วก็ไม่รู้ว่าแต่ละเมนูมีสารอาหารเท่าไหร่ กลุ่มของพวกเราจึงได้พัฒนาเว็บไซต์ที่ค้นหาอาหารที่บอกปริมาณสารอาหารของอาหารเมนูนั้นด้วยครับ</div>', unsafe_allow_html=True)
        st.markdown('<div class="subheader">| รายละเอียดเว็บไซต์</div>', unsafe_allow_html=True)
        st.markdown('<div class="passage">พวกเราได้สร้างเว็บไซต์สำหรับเลือกดูเมนูอาหาร โดยจะเน้นไปที่อาหารไทย ซึ่งเราก็จะสามารถหาดูอาหารพร้อมกับภาพประกอบ และข้อมูลโภชนาการให้เราได้เลือกรับประทานกันได้ง่าย ๆ ครับ</div>', unsafe_allow_html=True)
        st.markdown('<div class="subheader">| สมาชิก</div>', unsafe_allow_html=True)
        st.markdown('<div class="passage">1. นายปภพ กิตติภิญโญชัย (6634438223)</div>', unsafe_allow_html=True)
        st.markdown('<div class="passage">2. นายคุณานนต์ โสภาเจริญ (6634406123)</div>', unsafe_allow_html=True)
        st.markdown('<div class="passage">3. นายกีรติ แก้วโนนตุ่น (6634405523)</div>', unsafe_allow_html=True)
        st.markdown('<div class="subheader">| แหล่งอ้างอิงข้อมูลอาหาร</div>', unsafe_allow_html=True)
        st.markdown('<div class="passage"><a href="https://nutrition2.anamai.moph.go.th/th/thai-food-composition-table">ตารางแสดงคุณค่าทางโภชนาการอาหารไทย 2561 NUTRITIVE VALUES OF THAI FOODS</a>', unsafe_allow_html=True)

    def search_food_page(self):
        st.markdown('<div class="subheader2">🔎 ค้นหาเมนูอาหารทั้งหมด</div>', unsafe_allow_html=True)
        st.markdown('<div class="subheader3">💙 โปรดเลือกประเภทของเมนูอาหาร</div>', unsafe_allow_html=True)
        food_type = st.radio("| เลือกประเภทอาหาร : ", ["อาหารประเภทของคาว", "อาหารประเภทของหวาน"])
        if food_type == "อาหารประเภทของคาว":
            if st.button("ยืนยัน"):
                self.show_savory_page()

        elif food_type == "อาหารประเภทของหวาน":
            if st.button("ยืนยัน"):
                self.show_dessert_page()

    def nutritional_food_page(self):
        st.markdown('<div class="subheader2">🔎 ค้นหาเมนูอาหารตามโภชนาการ</div>', unsafe_allow_html=True)
        st.markdown('<div class="subheader3">💙 โปรดเลือกประเภทของเมนูอาหาร</div>', unsafe_allow_html=True)
        food_type = st.radio("| เลือกประเภทอาหาร", ["อาหารประเภทของคาว", "อาหารประเภทของหวาน"], key='nutritional_radio')
        if food_type == "อาหารประเภทของคาว":
            category = "savory"
        elif food_type == "อาหารประเภทของหวาน":
            category = "dessert"
        kcal = st.number_input("| ต้องการปริมาณพลังงานตั้งแต่ (kcal)", min_value=0)
        protein = st.number_input("| ต้องการปริมาณโปรตีนตั้งแต่ (g)", min_value=0)
        fat = st.number_input("| ต้องการปริมาณไขมันตั้งแต่ (g)", min_value=0)
        carbohydrate = st.number_input("| ต้องการปริมาณคาร์โบไฮเดรตตั้งแต่ (g)", min_value=0)
        button = st.button("ค้นหา")
        st.markdown(
        """<style>
            div[class*="stNumberInput"] label p {
            font-size: 25px;
            margin-bottom: 10px;
            color: #0D1282;
            font-family: 'Kanit', sans-serif;
        }</style>""", unsafe_allow_html=True)
        if button:
            self.show_nutritional_food_page(category, kcal, protein, fat, carbohydrate)

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
            
streamlit_app = StreamlitApp()
streamlit_app.run()