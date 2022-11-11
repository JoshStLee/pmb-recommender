import streamlit as st
import pandas as pd
import numpy as np
import pickle
import sklearn
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

special_model =  pickle.load(open('special_entry_model.sav', 'rb'))

st.title("Rekomendasi Pemilihan Mahasiswa Baru Jalur Prestasi")

with st.form("my_form"):
    kode_pendaftar = st.text_input("Kode Pendaftar","")
    provinsi_asal = st.selectbox("Provinsi Asal", daftar_provinsi[['provinsi']])
    container_for_selectbox = st.empty()
    container_for_optional_text = st.empty() 
    jurusan_sekolah = st.selectbox("Jurusan Sekolah",('IPA','IPS','Lainnya'))
    status_sekolah = st.selectbox("Status Sekolah",('NEGERI','SWASTA'))
    prodi_pilihan_1 = st.selectbox("Pilihan Prodi Pertama", daftar_prodi['nama_prodi'])
    prodi_pilihan_2 = st.selectbox("Pilihan Prodi Kedua", daftar_prodi['nama_prodi'])
    avg_nilai_uan = st.number_input("Rata-rata nilai UAN")
    avg_nilai_rapor = st.number_input("Rata-rata nilai rapor")
    
    
    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    container_when_submitted = st.empty()
    table_when_submitted = st.empty()
    
with container_for_selectbox:
    sekolah_asal = st.selectbox("Sekolah Asal",daftar_sekolah[['sekolah_asal']])    
    id_daftar_sekolah = daftar_sekolah.loc[daftar_sekolah['sekolah_asal']==sekolah_asal, 'id_daftar_sekolah'].iloc[0]    
with container_for_optional_text:
    if sekolah_asal == "TIDAK TERDAFTAR": 
        sekolah_asal = st.text_input("Masukkan nama sekolah")       
        if submitted:
            df2 = pd.DataFrame([[daftar_sekolah.index[-1]+1,sekolah_asal,status_sekolah]], 
                               columns=['id_daftar_sekolah','sekolah_asal','tipe_sekolah_asal'])
            daftar_sekolah = pd.concat([daftar_sekolah,df2])
            id_daftar_sekolah = daftar_sekolah.loc[daftar_sekolah['sekolah_asal']==sekolah_asal, 'id_daftar_sekolah'].iloc[0]

with container_when_submitted.container():     
    id_prodi_pilihan_1 = daftar_prodi.loc[daftar_prodi['nama_prodi']==prodi_pilihan_1, 'id_prodi'].iloc[0]
    id_prodi_pilihan_2 = daftar_prodi.loc[daftar_prodi['nama_prodi']==prodi_pilihan_2, 'id_prodi'].iloc[0]
    id_provinsi = daftar_provinsi.loc[daftar_provinsi['provinsi']==provinsi_asal, 'id_provinsi'].iloc[0]
    lokasi = 1 if id_provinsi>12 & id_provinsi<19 else 0
    tipe = 0 if jurusan_sekolah == 'Lainnya' else 1 
    status = 1 if status_sekolah =="NEGERI" else 0
    
test = {
        'lokasi':[lokasi],
        'status':[status],
        'tipe':[tipe],
        'id_daftar_sekolah':[id_daftar_sekolah],
        'id_prodi_pilihan_1':[id_prodi_pilihan_1],
        'id_prodi_pilihan_2':[id_prodi_pilihan_2],
        'avg_nilai_uan':[avg_nilai_uan],
        'avg_nilai_rapor':[avg_nilai_rapor],
       }

dummy = pd.DataFrame(test)

with table_when_submitted.container():
    if submitted:
        result = special_model.predict(dummy)[0]
        text_result = "DITERIMA" if result == 1 else "DITOLAK"
        st.write("HASIL ML", result, text_result)
        st.table(dummy)
