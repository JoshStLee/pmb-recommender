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

# st.session_state['option'] = 'Masukkan Opsi'
# if st.session_state['option']=='Masukkan Opsi' :
#     option = st.selectbox('Masukkan Jalur Registrasi', ('Masukkan Opsi','Jalur Reguler','Jalur Prestasi'))
    
# if(option=='Jalur Reguler'):
#     st.session_state['option']='Jalur Reguler'
#     # st.write("spawn the ML_NJP component here")
# elif(option=='Jalur Prestasi'):
#     st.session_state['option']='Jalur Prestasi'
#     st.write("spawn the ML_JP component here")
# if st.session_state['option']=='Jalur Reguler':
    
# if st.session_state['option']=='Jalur Prestasi':
    
# st.write(st.session_state['option']) 
