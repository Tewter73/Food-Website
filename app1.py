import streamlit as st
from streamlit_option_menu import option_menu

selected = option_menu(
    menu_title = "Main Menu",
    options = ["Home","Projects","Contract"],
    icons = ["house","book","envelope"],
    menu_icon = "cast",
    default_index = 0,
    orientation = "horizontal",
)


if selected == "Home":
    st.title(f"You have selected {selected}")
if selected == "Projects":
    st.title(f"You have selected {selected}")
if selected == "Contract":
    st.title(f"You have selected {selected}")