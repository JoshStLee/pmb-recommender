import streamlit as st
import pandas as pd
import numpy as np
st.title('PMB Recommender Test')
jp = pd.read_csv('data_jp.csv')
njp = pd.read_csv('data_njp.csv')
option = st.selectbox(
    'Masukkan Jalur Registrasi',
    ('Masukkan Opsi','Jalur Reguler','Jalur Prestasi'))
if(option=='Jalur Reguler'):
    st.write("spawn the ML_NJP component here")
elif(option=='Jalur Prestasi'):
    st.write("spawn the ML_JP component here")