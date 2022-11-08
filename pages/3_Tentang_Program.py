import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
icon = Image.open('icon_ukdw.png')

st.set_page_config(
    page_title= "Tentang Program",
    page_icon= icon
)
st.title("Tentang Maket Program")
st.write("dikembangkan sebagai implementasi metodologi skripsi")
st.write("Joshua Putra Setyadi (71170173)")
st.write("Universitas Kristen Duta Wacana")