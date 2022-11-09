import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
icon = Image.open('icon_ukdw.png')


daftar_sekolah = pd.read_csv('daftar_sekolah.csv')[['id_daftar_sekolah','sekolah_asal','tipe_sekolah_asal']]
daftar_provinsi = pd.read_csv('daftar_provinsi.csv')
daftar_prodi = pd.read_csv('daftar_prodi.csv')

st.set_page_config(
    page_title= "Rekomendasi Seleksi Prestasi",
    page_icon= icon,
    initial_sidebar_state = "collapsed"
)

st.title("Rekomendasi Pemilihan Mahasiswa Baru Jalur Reguler")

with st.form("my_form"):
    kode_pendaftar = st.text_input("Kode Pendaftar","")
    provinsi_asal = st.selectbox("Provinsi Asal", daftar_provinsi[['provinsi']])
    container_for_selectbox = st.empty()
    container_for_optional_text = st.empty() 
    jurusan_sekolah = st.selectbox("Jurusan Sekolah",('IPA','IPS','Lainnya'))
    status_sekolah = st.selectbox("Status Sekolah",('NEGERI','SWASTA'))
    prodi_pilihan_1 = st.selectbox("Pilihan Prodi Pertama", daftar_prodi['nama_prodi'])
    prodi_pilihan_1 = st.selectbox("Pilihan Prodi Kedua", daftar_prodi['nama_prodi'])
    avg_nilai_uan = st.number_input("Rata-rata nilai UAN")
    avg_nilai_rapor = st.number_input("Rata-rata nilai rapor")
    
    
    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    # if submitted:
    #     # st.session_state['']
    #     st.write("slider", slider_val, "checkbox", checkbox_val)

with container_for_selectbox:
    sekolah_asal = st.selectbox("Sekolah Asal",daftar_sekolah[['sekolah_asal']])
    
with container_for_optional_text:
    if sekolah_asal == "TIDAK TERDAFTAR": 
        sekolah_asal = st.text_input("Masukkan nama sekolah")