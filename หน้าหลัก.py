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
  
    def run(self):
        self.home_page()

    def home_page(self):
        st.markdown('<div class="home">🏠 หน้าหลัก</div>', unsafe_allow_html=True)
        st.markdown('<div class="header">🍔 เกี่ยวกับเว็บไซต์ของเรา</div>', unsafe_allow_html=True)
        st.markdown('<div class="subheader">| เหตุผลในการพัฒนา :</div>', unsafe_allow_html=True)
        st.markdown('<div class="passage">บางครั้งเมื่อเราออกกำลังกาย และต้องการอยากที่จะคุมอาหารเพื่อสุขภาพที่ดี เราต้องการที่จะทราบถึงปริมาณสารอาหารที่เหมาะสมกับตัวเรา แล้วก็ไม่รู้ว่าแต่ละเมนูมีสารอาหารเท่าไหร่ กลุ่มของพวกเราจึงได้พัฒนาเว็บไซต์ที่ค้นหาอาหารที่บอกปริมาณสารอาหารของอาหารเมนูนั้นด้วยครับ</div>', unsafe_allow_html=True)
        st.markdown('<div class="subheader">| รายละเอียดเว็บไซต์</div>', unsafe_allow_html=True)
        st.markdown('<div class="passage">พวกเราได้สร้างเว็บไซต์สำหรับเลือกดูเมนูอาหาร โดยจะเน้นไปที่อาหารไทย ซึ่งเราก็จะสามารถหาดูอาหารพร้อมกับภาพประกอบ และข้อมูลโภชนาการให้เราได้เลือกรับประทานกันได้ง่าย ๆ ครับ</div>', unsafe_allow_html=True)
        st.markdown('<div class="subheader">| สมาชิก</div>', unsafe_allow_html=True)
        st.markdown('<div class="passage">1. นายปภพ กิตติภิญโญชัย (6634438223)</div>', unsafe_allow_html=True)
        st.markdown('<div class="passage">2. นายคุณานนต์ โสภาเจริญ (6634406123)</div>', unsafe_allow_html=True)
        st.markdown('<div class="passage">3. นายกีรติ แก้วโนนตุ่น (6634405523)</div>', unsafe_allow_html=True)
        st.markdown('<div class="subheader">| แหล่งอ้างอิงข้อมูลอาหาร : </div>', unsafe_allow_html=True)
        st.markdown('<div class="passage"><a href="https://nutrition2.anamai.moph.go.th/th/thai-food-composition-table">ตารางแสดงคุณค่าทางโภชนาการอาหารไทย 2561 NUTRITIVE VALUES OF THAI FOODS</a>', unsafe_allow_html=True)

   
streamlit_app = StreamlitApp()
streamlit_app.run()