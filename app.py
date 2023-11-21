# ทำการ Activate Python Virtual Environment ด้วยคำสั่ง env\Scripts\activate ก่อน
# pip freeze > requirements.txt เพื่อส่งไฟล์ให้คนอื่น
import streamlit as st
import sqlite3
from PIL import Image
import random

# ตั้งค่าหน้าเว็บ Streamlit
st.set_page_config(
    page_title="วันนี้กินไรดี?",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded",
)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

class Database:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def execute_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close_connection(self):
        self.conn.close()

local_css("style.css")

class FoodApp:
    def __init__(self):
        self.selected_page = None
        self.categories = ["หน้าหลัก", "ค้นหาเมนูอาหารทั้งหมด", "เลือกเมนูอาหารตามโภชนาการ", "สุ่มอาหาร"]
        self.database = Database('database.db')

    def run(self):
        self.selected_page = st.sidebar.selectbox("ไปยัง", self.categories)

        if self.selected_page == "หน้าหลัก":
            self.home_page()
        elif self.selected_page == "ค้นหาเมนูอาหารทั้งหมด":
            self.search_recipe_page()
        elif self.selected_page == "เลือกเมนูอาหารตามโภชนาการ":
            self.nutritional_recipe_page()
        elif self.selected_page == "สุ่มอาหาร":
            self.random_recipe_page()

    def load_food_data(self, category):
        query = f"SELECT id, name, kcal, protein, fat, carbohydrate FROM {category};"
        return self.database.execute_query(query)

    def load_food_data_with_nutrition(self, category):
        return self.load_food_data(category)

    def show_image_and_nutrition(self, food_id, food_name, category):
        image_path = f'images/{category}_images/{food_id}.jpg'

        try:
            img = Image.open(image_path)
            st.image(img, caption=None, use_column_width=False , width=200)
            food_data = self.load_food_data(category)
            for id, name, kcal, protein, fat, carbohydrate in food_data:
                if id == food_id:
                    st.write(f'**ปริมาณพลังงาน (kcal):** {kcal}')
                    st.write(f'**ปริมาณโปรตีน (g):** {protein}')
                    st.write(f'**ปริมาณไขมัน (g):** {fat}')
                    st.write(f'**ปริมาณคาร์โบไฮเดรต (g):** {carbohydrate}')
                    break       

        except FileNotFoundError:
            st.warning(f'ไม่พบรูปภาพสำหรับ {food_name}')

    def show_savory_page(self):
        st.title('เมนูอาหารประเภทของคาว')
        savory_data = self.load_food_data_with_nutrition('savory')
        for food_id, food_name, _, _, _, _ in savory_data:
            st.write(food_name)
            self.show_image_and_nutrition(food_id, food_name, 'savory')

    def show_dessert_page(self):
        st.title('เมนูอาหารประเภทของหวาน')
        sweet_data = self.load_food_data_with_nutrition('dessert')
        for food_id, food_name, _, _, _, _ in sweet_data:
            st.write(food_name)
            self.show_image_and_nutrition(food_id, food_name, 'dessert')

    def show_nutritional_food_page(self, category, kcal, protein, fat, carbohydrate):
        food_data = self.load_food_data(category)

        if kcal is None or protein is None or fat is None or carbohydrate is None:
            st.error("กรุณากรอกปริมาณสารอาหารอย่างน้อยหนึ่งรายการ")
        else:
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
                st.error("ไม่พบเมนูอาหารที่ท่านต้องการ")
            else:
                for food_id, food_name in filtered_food_data:
                    st.write(food_name)
                    self.show_image_and_nutrition(food_id, food_name, category)

    def show_random_food(self, category):
        st.title("เมนูอาหารสำหรับคุณในมือนี้ ก็คือ!!!")

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

    def search_recipe_page(self):
        st.title("โปรดเลือกประเภทของเมนูอาหาร")
        food_type = st.radio("เลือกประเภทอาหาร", ["อาหารประเภทของคาว", "อาหารประเภทของหวาน"])
        if food_type == "อาหารประเภทของคาว":
            if st.button("ยืนยัน"):
                self.show_savory_page()

        elif food_type == "อาหารประเภทของหวาน":
            if st.button("ยืนยัน"):
                self.show_dessert_page()

    def nutritional_recipe_page(self):
        st.title("โปรดเลือกประเภทของเมนูอาหาร")
        food_type = st.radio("เลือกประเภทอาหาร", ["อาหารประเภทของคาว", "อาหารประเภทของหวาน"])
        if food_type == "อาหารประเภทของคาว":
            category = "savory"
        elif food_type == "อาหารประเภทของหวาน":
            category = "dessert"

        # แสดงช่องกรอกข้อมูลปริมาณสารอาหาร
        kcal = st.number_input("ปริมาณพลังงานต้องมากกว่า (kcal)", min_value=0)
        protein = st.number_input("ปริมาณโปรตีนต้องมากกว่า (g)", min_value=0)
        fat = st.number_input("ปริมาณไขมันต้องมากกว่า (g)", min_value=0)
        carbohydrate = st.number_input("ปริมาณคาร์โบไฮเดรตต้องมากกว่า (g)", min_value=0)

        # แสดงปุ่มเดียว
        button = st.button("ค้นหา")

        if button:
            self.show_nutritional_food_page(category, kcal, protein, fat, carbohydrate)

    def random_recipe_page(self):
        st.title("สุ่มอาหาร")
        st.title("โปรดเลือกประเภทของเมนูอาหาร")
        food_type = st.radio("เลือกประเภทอาหาร", ["อาหารประเภทของคาว", "อาหารประเภทของหวาน"])
        if food_type == "อาหารประเภทของคาว":
            if st.button("สุ่มเมนู"):
                self.show_random_food('savory')
        elif food_type == "อาหารประเภทของหวาน":
            if st.button("สุ่มเมนู"):
                self.show_random_food('dessert')

# สร้าง instance ของ FoodApp และเรียก run method
food_app = FoodApp()
food_app.run()