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
    page_title= "Rekomendasi Seleksi Prestasi",
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
    
if "data_baru_prestasi" not in st.session_state:
    st.session_state.data_baru_prestasi = pd.DataFrame(columns=['lokasi','status','tipe',
                                                                'id_daftar_sekolah',
                                                                'id_prodi_pilihan_1',
                                                                'id_prodi_pilihan_2',
                                                                'avg_nilai_uan',
                                                                'avg_nilai_raport',
                                                                'is_diterima'])

daftar_sekolah = st.session_state.daftar_sekolah
daftar_sekolah.id_lokasi=daftar_sekolah.id_lokasi.fillna(0).astype(int)
daftar_provinsi = pd.read_csv('daftar_provinsi.csv')
daftar_prodi = pd.read_csv('daftar_prodi.csv')
daftar_lokasi = pd.read_csv('daftar_lokasi.csv')
special_model =  pickle.load(open('special_entry_model.sav', 'rb'))

jp = pd.read_csv('data_jp_legit.csv')
y = jp[['is_diterima']]
X = jp.drop(['is_diterima'], axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.4, random_state = 42)
    
st.title("Rekomendasi Seleksi Mahasiswa Baru Jalur Prestasi")

with st.form("my_form"):
    container_for_selectbox = st.empty()
    container_for_optional_text = st.empty() 
    jurusan_sekolah = st.selectbox("Jurusan Sekolah",('IPA','IPS','Lainnya'))
    prodi_pilihan_1 = st.selectbox("Pilihan Prodi Pertama", daftar_prodi['nama_prodi'])
    prodi_pilihan_2 = st.selectbox("Pilihan Prodi Kedua", daftar_prodi['nama_prodi'])
    avg_nilai_uan = st.number_input("Rata-rata nilai UAN", step=0.1)
    avg_nilai_rapor = st.number_input("Rata-rata nilai rapor", step=0.1)
    
    submitted = st.form_submit_button("Submit")
    
with container_for_selectbox:
    sekolah_asal = st.selectbox("Sekolah Asal",daftar_sekolah[['sekolah_asal']])    
    id_daftar_sekolah = daftar_sekolah.loc[daftar_sekolah['sekolah_asal']==sekolah_asal,
                                           'id_daftar_sekolah'].iloc[0]    
    
with container_for_optional_text:
    if sekolah_asal != "TIDAK TERDAFTAR": 
        container_for_optional_text.empty()
    elif sekolah_asal == "TIDAK TERDAFTAR":    
        with st.form("school_form"):
            nama_sekolah = st.text_input("Bila tidak terdaftar, masukkan nama sekolah")
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

if submitted:
    id_daftar_sekolah = daftar_sekolah.loc[daftar_sekolah['sekolah_asal']==sekolah_asal,
                                               'id_daftar_sekolah'].iloc[0]    
    id_prodi_pilihan_1 = daftar_prodi.loc[daftar_prodi['nama_prodi']==prodi_pilihan_1, 'id_prodi'].iloc[0]
    id_prodi_pilihan_2 = daftar_prodi.loc[daftar_prodi['nama_prodi']==prodi_pilihan_2, 'id_prodi'].iloc[0]
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
        'avg_nilai_uan':[avg_nilai_uan],
        'avg_nilai_raport':[avg_nilai_rapor],
    })

    # write the decision paths taken by the ML
    with st.expander("Penghitungan Keputusan ML"):
        n_nodes_ = [t.tree_.node_count for t in special_model.estimators_]
        children_left_ = [t.tree_.children_left for t in special_model.estimators_]
        children_right_ = [t.tree_.children_right for t in special_model.estimators_]
        feature_ = [t.tree_.feature for t in special_model.estimators_]
        threshold_ = [t.tree_.threshold for t in special_model.estimators_]
        positive_counter = 0
        tabs_list = []
        tabs_for_decision = st.empty()
        for i,e in enumerate(special_model.estimators_):
            tabs_list.append("Tree %d\n"%(i+1))
            with tabs_for_decision.container():    
                output = special_model.estimators_[i].predict(test)[0]
                if output == 1:
                    positive_counter+=1
                tabs = st.tabs(tabs_list)
                with tabs[i]:
                    explore_tree(X, test, special_model.estimators_[i], n_nodes_[i], children_left_[i], 
                                 children_right_[i], feature_[i],threshold_[i], suffix=i, 
                                 sample_id=0)
    # show predicted result
    result = special_model.predict(test)[0]
    st.write("%s"% (positive_counter*12.5)+"% DT memberikan rekomendasi" )
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
        'avg_nilai_uan':[avg_nilai_uan],
        'avg_nilai_raport':[avg_nilai_rapor],
        'is_diterima': [result]
    })
    
    st.session_state.data_baru_prestasi = pd.concat([st.session_state.data_baru_prestasi, 
                                                    entry], ignore_index=True) 
    
# show form data, download data, and retrain model                
if st.session_state.data_baru_prestasi.shape[0] :   
    if st.button('Tampilkan Data Keluaran'):
        st.write(st.session_state.data_baru_prestasi)
    
    data_luaran = convert_df(st.session_state.data_baru_prestasi)
    save_data = st.download_button(
        label="Unduh Data Keluaran",
        data=data_luaran,
        file_name='output_rekomendasi_jalur_prestasi.csv',
        mime='text/csv',
    )
    if save_data :
        st.session_state.data_baru_prestasi.drop(st.session_state.data_baru_prestasi.index, inplace=True)
            
with st.expander("Langkah untuk Latih Ulang Model"):
    uploaded_data = st.file_uploader("Unggah Data Latih Baru Untuk ML")
    if uploaded_data is not None:
        data_latih = pd.read_csv(uploaded_data)
        st.write("Data Unggahan")
        st.dataframe(data_latih)
        if st.button('Latih Ulang Model'):
            retrain_ml(X_train, y_train, data_latih, special_model)
