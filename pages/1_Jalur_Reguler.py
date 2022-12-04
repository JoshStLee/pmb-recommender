import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from PIL import Image
from functions import *

icon = Image.open('icon_ukdw.png')

st.set_page_config(
    page_title= "Rekomendasi Seleksi Reguler",
    page_icon= icon,
    initial_sidebar_state = "collapsed"
)

@st.cache
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

if "daftar_sekolah" not in st.session_state :
    st.session_state.daftar_sekolah = pd.read_csv('daftar_sekolah.csv')[['id_daftar_sekolah',
                                                                         'id_lokasi',
                                                                         'sekolah_asal',
                                                                         'tipe_sekolah_asal',                                           
                                                                         'jenis_sekolah']]
    
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
daftar_sekolah.id_lokasi=daftar_sekolah.id_lokasi.fillna(0).astype(int)
daftar_provinsi = pd.read_csv('daftar_provinsi.csv')
daftar_prodi = pd.read_csv('daftar_prodi.csv')
daftar_lokasi = pd.read_csv('daftar_lokasi.csv')
regular_model =  pickle.load(open('regular_entry_model.sav', 'rb'))
new_school_entry = 0

njp = pd.read_csv('data_njp.csv')
y = njp[['is_diterima']]
X = njp.drop(['is_diterima'], axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.4, random_state = 42)

st.title("Rekomendasi Seleksi Mahasiswa Baru Jalur Reguler")

with st.form("my_form"):
    container_for_selectbox = st.empty()
    container_for_optionals = st.empty() 
    jurusan_sekolah = st.selectbox("Jurusan Sekolah",('IPA','IPS','BAHASA','LAINNYA'))
    prodi_pilihan_1 = st.selectbox("Pilihan Prodi Pertama", daftar_prodi['nama_prodi'])
    prodi_pilihan_2 = st.selectbox("Pilihan Prodi Kedua", daftar_prodi['nama_prodi'])
    nilai_tpa_verbal = st.number_input("Nilai TPA Verbal", step=1)
    nilai_tpa_spasial = st.number_input("Nilai TPA Spasial", step=1)
    nilai_tpa_analogi = st.number_input("Nilai TPA Analogi", step=1)
    nilai_tpa_numerik = st.number_input("Nilai TPA Numerik", step=1)
            
    submitted = st.form_submit_button("Submit")
 
    
with container_for_selectbox:   
    sekolah_asal = st.selectbox("Sekolah Asal",daftar_sekolah[['sekolah_asal']]) 
    
with container_for_optionals:
    if sekolah_asal == "TIDAK TERDAFTAR": 
        with st.form("school_form"):
            nama_sekolah = st.text_input("Bila sekolah tidak terdaftar, masukkan nama sekolah")
            jenis_sekolah = st.selectbox("Jenis Sekolah",('SMA','SMK','HOMESCHOOLING','LUAR NEGERI','PKBM'))
            provinsi= st.selectbox("Provinsi Sekolah", daftar_provinsi[['provinsi']])
            lokasi_asal = st.selectbox("Kota/Kabupaten Sekolah", daftar_lokasi["kabupaten_kota"])
            status_sekolah = st.selectbox("Status Sekolah",('NEGERI','SWASTA'))
            school_submitted = st.form_submit_button("Masukkan ke daftar")
            if school_submitted:    
                sekolah_asal = nama_sekolah.upper()
                id_lokasi = daftar_lokasi.loc[daftar_lokasi["kabupaten_kota"]==lokasi_asal,"id_lokasi"]
                df = pd.DataFrame([[daftar_sekolah.index[-1]+1,id_lokasi,sekolah_asal,status_sekolah,jenis_sekolah]], 
                                  columns=['id_daftar_sekolah','id_lokasi',
                                           'sekolah_asal',
                                           'tipe_sekolah_asal',                                                                  
                                           'jenis_sekolah'])
                daftar_sekolah = pd.concat([daftar_sekolah,df], ignore_index=True)
                id_daftar_sekolah = daftar_sekolah.loc[daftar_sekolah['sekolah_asal']==sekolah_asal, 
                                                       'id_daftar_sekolah'].iloc[0]
                st.session_state.daftar_sekolah = daftar_sekolah
                with container_for_selectbox:
                    sekolah_asal = st.selectbox("Sekolah Asal",daftar_sekolah[['sekolah_asal']],
                                                index=daftar_sekolah.index[-1]) 
                container_for_optionals.empty()
                    

if submitted:
    id_prodi_pilihan_1 = daftar_prodi.loc[daftar_prodi['nama_prodi']==prodi_pilihan_1, 'id_prodi'].iloc[0]
    id_prodi_pilihan_2 = daftar_prodi.loc[daftar_prodi['nama_prodi']==prodi_pilihan_2, 'id_prodi'].iloc[0]
    id_daftar_sekolah = daftar_sekolah.loc[daftar_sekolah['sekolah_asal']==sekolah_asal, 
                                               'id_daftar_sekolah'].iloc[0] 
    id_lokasi = daftar_sekolah.loc[daftar_sekolah['sekolah_asal']==sekolah_asal, 'id_lokasi'].iloc[0]
    status_sekolah = daftar_sekolah.loc[daftar_sekolah['sekolah_asal']==sekolah_asal, 'tipe_sekolah_asal'].iloc[0]
    jenis_sekolah = daftar_sekolah.loc[daftar_sekolah['sekolah_asal']==sekolah_asal, 'jenis_sekolah'].iloc[0]
    lokasi = 1 if ((id_lokasi>154) & (id_lokasi<255)) else 0
    tipe = 1 if jenis_sekolah == 'SMA' else 0
    status = 1 if status_sekolah =="NEGERI" else 0
    
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

    # write the decision paths taken by the ML
    with st.expander("Perhitungan Keputusan ML"):
        n_nodes_ = [t.tree_.node_count for t in regular_model.estimators_]
        children_left_ = [t.tree_.children_left for t in regular_model.estimators_]
        children_right_ = [t.tree_.children_right for t in regular_model.estimators_]
        feature_ = [t.tree_.feature for t in regular_model.estimators_]
        threshold_ = [t.tree_.threshold for t in regular_model.estimators_]
        positive_counter = 0
        tabs_list = []
        tabs_for_decision = st.empty() 

        for i,e in enumerate(regular_model.estimators_):
            tabs_list.append("Tree %d\n"%(i+1))
            with tabs_for_decision.container():    
                output = regular_model.estimators_[i].predict(test)[0]
                if output == 1:
                    positive_counter+=1
                tabs = st.tabs(tabs_list)
                with tabs[i]:
                    explore_tree(X, test, regular_model.estimators_[i], n_nodes_[i], children_left_[i], 
                                 children_right_[i], feature_[i],threshold_[i], suffix=i, 
                                 sample_id=0)
    
    # show predicted result
    result = regular_model.predict(test)[0]
    st.write("%s"% (positive_counter*10)+"% DT memberikan rekomendasi" )
    text_result = "DITERIMA" if result else "DITOLAK"
    st.write("HASIL AKHIR ML: "+ text_result)
    
    # save the data for download
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

# show form data, download data, and retrain model
if st.session_state.data_baru_reguler.shape[0] :   
    if st.button('Tampilkan Data Keluaran'):
        st.write(st.session_state.data_baru_reguler)
        
    
    data_luaran = convert_df(st.session_state.data_baru_reguler)
    save_data = st.download_button(
        label="Unduh Data Keluaran",
        data=data_luaran,
        file_name='output_rekomendasi_jalur_reguler.csv',
        mime='text/csv',
    )
    if save_data :
        st.session_state.data_baru_reguler.drop(st.session_state.data_baru_reguler.index, inplace=True)
            
with st.expander("Langkah untuk Latih Ulang Model"):
    uploaded_data = st.file_uploader("Unggah Data Latih Baru Untuk ML")
    if uploaded_data is not None:
        data_latih = pd.read_csv(uploaded_data)
        st.write("Data Unggahan")
        st.dataframe(data_latih)
        if st.button('Latih Ulang Model'):
            retrain_ml(X_train, y_train.values.ravel(), data_latih, regular_model)
        