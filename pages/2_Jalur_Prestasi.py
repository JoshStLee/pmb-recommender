import streamlit as st
from PIL import Image
icon = Image.open('icon_ukdw.png')

st.set_page_config(
    page_title= "Rekomendasi Seleksi Prestasi",
    page_icon= icon
)