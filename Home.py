import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
icon = Image.open('icon_ukdw.png')

st.set_page_config(
    page_title= "PMB Recommender Test",
    page_icon= icon
)
st.title("Selamat Datang di Program Rekomendasi PMB FTI UKDW")
st.write("👈 Pilih jalur registrasi data pada sidebar")
