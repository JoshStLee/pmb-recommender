import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from PIL import Image
from sklearn.model_selection import train_test_split
icon = Image.open('icon_ukdw.png')

st.set_page_config(
    page_title= "Rekomendasi Seleksi Reguler",
    page_icon= icon,
    initial_sidebar_state = "collapsed"
)

if "daftar_sekolah" not in st.session_state :
    st.session_state.daftar_sekolah = pd.read_csv('daftar_sekolah.csv')[['id_daftar_sekolah',
                                                                         'sekolah_asal',
                                                                         'tipe_sekolah_asal']]
    
if "data_baru_reguler" not in st.session_state:
    st.session_state.data_baru_reguler = pd.DataFrame(columns=['lokasi','status','tipe',
                                                       'id_daftar_sekolah',
                                                       'id_prodi_pilihan_1',
                                                       'id_prodi_pilihan_2',
                                                       'nilai_tpa_verbal',
                                                       'nilai_tpa_spasial',
                                                       'nilai_tpa_analogi',
                                                       'nilai_tpa_numerik',
                                                       'is_diterima'])
    
daftar_sekolah = st.session_state.daftar_sekolah
daftar_provinsi = pd.read_csv('daftar_provinsi.csv')
daftar_prodi = pd.read_csv('daftar_prodi.csv')
regular_model = RandomForestClassifier(n_estimators=10)
regular_model =  pickle.load(open('regular_entry_model.sav', 'rb'))
njp = pd.read_csv('data_njp.csv')
y = njp[['is_diterima']]
X = njp.drop(['is_diterima'], axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.4, random_state = 42)

def retrain_ml(X_train, y_train, regular_model):
    train_baru = st.session_state.data_baru_reguler.drop(['is_diterima'],axis=1)
    class_baru = st.session_state.data_baru_reguler[['is_diterima']]
    X_train = pd.concat([X_train,train_baru], ignore_index=True)
    y_train = pd.concat([y_train,class_baru], ignore_index=True)
    regular_model.fit(X_train.astype(int), y_train.astype(int))
    st.session_state.data_baru_reguler.drop(st.session_state.data_baru_reguler.index, inplace=True)  

st.title("Rekomendasi Pemilihan Mahasiswa Baru Jalur Reguler")

with st.form("my_form", clear_on_submit=True):
    kode_pendaftar = st.text_input("Kode Pendaftar","")
    provinsi_asal = st.selectbox("Provinsi Asal", daftar_provinsi[['provinsi']])
    container_for_selectbox = st.empty()
    container_for_optional_text = st.empty() 
    jurusan_sekolah = st.selectbox("Jurusan Sekolah",('IPA','IPS','LAINNYA'))
    status_sekolah = st.selectbox("Status Sekolah",('NEGERI','SWASTA'))
    prodi_pilihan_1 = st.selectbox("Pilihan Prodi Pertama", daftar_prodi['nama_prodi'])
    prodi_pilihan_2 = st.selectbox("Pilihan Prodi Kedua", daftar_prodi['nama_prodi'])
    nilai_tpa_verbal = st.number_input("Nilai TPA Verbal", step=1)
    nilai_tpa_spasial = st.number_input("Nilai TPA Spasial", step=1)
    nilai_tpa_analogi = st.number_input("Nilai TPA Analogi", step=1)
    nilai_tpa_numerik = st.number_input("Nilai TPA Numerik", step=1)
            
    submitted = st.form_submit_button("Submit")
    container_when_submitted = st.empty()
    id_prodi_pilihan_1 = daftar_prodi.loc[daftar_prodi['nama_prodi']==prodi_pilihan_1, 'id_prodi'].iloc[0]
    id_prodi_pilihan_2 = daftar_prodi.loc[daftar_prodi['nama_prodi']==prodi_pilihan_2, 'id_prodi'].iloc[0]
    id_provinsi = daftar_provinsi.loc[daftar_provinsi['provinsi']==provinsi_asal, 'id_provinsi'].iloc[0]
    lokasi = 1 if id_provinsi>12 & id_provinsi<19 else 0
    tipe = 0 if jurusan_sekolah == 'Lainnya' else 1 
    status = 1 if status_sekolah =="NEGERI" else 0
    
with container_for_selectbox:
    sekolah_asal = st.selectbox("Sekolah Asal",daftar_sekolah[['sekolah_asal']])   
    id_daftar_sekolah = daftar_sekolah.loc[daftar_sekolah['sekolah_asal']==sekolah_asal, 
                                               'id_daftar_sekolah'].iloc[0]    

with container_for_optional_text:
    if sekolah_asal == "TIDAK TERDAFTAR": 
        sekolah_asal = st.text_input("Masukkan nama sekolah")       
        if submitted:
            df = pd.DataFrame([[daftar_sekolah.index[-1]+1,sekolah_asal,status_sekolah]], 
                              columns=['id_daftar_sekolah','sekolah_asal','tipe_sekolah_asal'])
            daftar_sekolah = pd.concat([daftar_sekolah,df], ignore_index=True)
            id_daftar_sekolah = daftar_sekolah.loc[daftar_sekolah['sekolah_asal']==sekolah_asal, 
                                                   'id_daftar_sekolah'].iloc[0]
            st.session_state.daftar_sekolah = daftar_sekolah
                #session state now saves the new school list
        
with container_when_submitted.container():       
    test = pd.DataFrame({
        'lokasi':[lokasi],
        'status':[status],
        'tipe':[tipe],
        'id_daftar_sekolah':[id_daftar_sekolah],
        'id_prodi_pilihan_1':[id_prodi_pilihan_1],
        'id_prodi_pilihan_2':[id_prodi_pilihan_2],
        'nilai_tpa_verbal':[nilai_tpa_verbal],
        'nilai_tpa_spasial':[nilai_tpa_spasial],
        'nilai_tpa_analogi':[nilai_tpa_analogi],
        'nilai_tpa_numerik':[nilai_tpa_numerik]
       })

    if submitted:
        result = regular_model.predict(test)[0]
        text_result = "DITERIMA" if result == 1 else "DITOLAK"
        st.write("HASIL ML", text_result)
        
        entry = pd.DataFrame({
            'lokasi':[lokasi],
            'status':[status],
            'tipe':[tipe],
            'id_daftar_sekolah':[id_daftar_sekolah],
            'id_prodi_pilihan_1':[id_prodi_pilihan_1],
            'id_prodi_pilihan_2':[id_prodi_pilihan_2],
            'nilai_tpa_verbal':[nilai_tpa_verbal],
            'nilai_tpa_spasial':[nilai_tpa_spasial],
            'nilai_tpa_analogi':[nilai_tpa_analogi],
            'nilai_tpa_numerik':[nilai_tpa_numerik],
            'is_diterima':[result]
        })
        
        st.session_state.data_baru_reguler = pd.concat([st.session_state.data_baru_reguler, 
                                                        entry], ignore_index=True) 
        with container_for_selectbox:
            sekolah_asal = st.selectbox("Sekolah Asal",daftar_sekolah[['sekolah_asal']])   
            id_daftar_sekolah = daftar_sekolah.loc[daftar_sekolah['sekolah_asal']==sekolah_asal, 
                                                       'id_daftar_sekolah'].iloc[0]    
        with container_for_optional_text:
            if sekolah_asal == "TIDAK TERDAFTAR": 
                sekolah_asal = st.text_input("Masukkan nama sekolah")       
                if submitted:
                    df = pd.DataFrame([[daftar_sekolah.index[-1]+1,sekolah_asal,status_sekolah]], 
                                      columns=['id_daftar_sekolah','sekolah_asal','tipe_sekolah_asal'])
                    daftar_sekolah = pd.concat([daftar_sekolah,df], ignore_index=True)
                    id_daftar_sekolah = daftar_sekolah.loc[daftar_sekolah['sekolah_asal']==sekolah_asal, 
                                                           'id_daftar_sekolah'].iloc[0]
                    st.session_state.daftar_sekolah = daftar_sekolah
                        #session state now saves the new school list
        
if st.session_state.data_baru_reguler.shape[0]  >= 5:
    if st.button('latih ulang ML'):
        retrain_ml(X_train, y_train, regular_model)
        
            