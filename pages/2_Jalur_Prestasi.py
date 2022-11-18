import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from PIL import Image

icon = Image.open('icon_ukdw.png')

st.set_page_config(
    page_title= "Rekomendasi Seleksi Prestasi",
    page_icon= icon,
    initial_sidebar_state = "collapsed"
)

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')

if "daftar_sekolah" not in st.session_state :
    st.session_state.daftar_sekolah = pd.read_csv('daftar_sekolah.csv')[['id_daftar_sekolah',
                                                                         'sekolah_asal',
                                                                         'tipe_sekolah_asal']]
    
if "data_baru_prestasi" not in st.session_state:
    st.session_state.data_baru_prestasi = pd.DataFrame(columns=['lokasi','status','tipe',
                                                                'id_daftar_sekolah',
                                                                'id_prodi_pilihan_1',
                                                                'id_prodi_pilihan_2',
                                                                'avg_nilai_uan',
                                                                'avg_nilai_rapor',
                                                                'is_diterima'])

daftar_sekolah = st.session_state.daftar_sekolah
daftar_provinsi = pd.read_csv('daftar_provinsi.csv')
daftar_prodi = pd.read_csv('daftar_prodi.csv')
special_model =  pickle.load(open('special_entry_model.sav', 'rb'))
jp = pd.read_csv('data_jp_legit.csv')
y = jp[['is_diterima']]
X = jp.drop(['is_diterima'], axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.4, random_state = 42)

def retrain_ml(X_train, y_train, data_baru, model):
    train_baru = data_baru.drop(['is_diterima'],axis=1)
    class_baru = data_baru[['is_diterima']]
    X_train = pd.concat([X_train,train_baru], ignore_index=True)
    y_train = pd.concat([y_train,class_baru], ignore_index=True)
    model.fit(X_train.astype(int), y_train.astype(int))
    st.write("data dilatih")
    
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
    
    submitted = st.form_submit_button("Submit")
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
            df2 = pd.DataFrame([[daftar_sekolah.index[-1]+1,sekolah_asal,status_sekolah]], 
                               columns=['id_daftar_sekolah','sekolah_asal','tipe_sekolah_asal'])
            daftar_sekolah = pd.concat([daftar_sekolah,df2], ignore_index=True)
            id_daftar_sekolah = daftar_sekolah.loc[daftar_sekolah['sekolah_asal']==sekolah_asal, 
                                                   'id_daftar_sekolah'].iloc[0]
            st.session_state.daftar_sekolah = daftar_sekolah
    
test = pd.DataFrame({
    'lokasi':[lokasi],
    'status':[status],
    'tipe':[tipe],
    'id_daftar_sekolah':[id_daftar_sekolah],
    'id_prodi_pilihan_1':[id_prodi_pilihan_1],
    'id_prodi_pilihan_2':[id_prodi_pilihan_2],
    'avg_nilai_uan':[avg_nilai_uan],
    'avg_nilai_rapor':[avg_nilai_rapor],
   })

if submitted:
    result = special_model.predict(dummy)[0]
    text_result = "DITERIMA" if result == 1 else "DITOLAK"
    st.write("HASIL ML", result, text_result)

    entry = pd.DataFrame({
        'lokasi':[lokasi],
        'status':[status],
        'tipe':[tipe],
        'id_daftar_sekolah':[id_daftar_sekolah],
        'id_prodi_pilihan_1':[id_prodi_pilihan_1],
        'id_prodi_pilihan_2':[id_prodi_pilihan_2],
        'avg_nilai_uan':[avg_nilai_uan],
        'avg_nilai_rapor':[avg_nilai_rapor],
        'is_diterima': [result]
    })
    
    st.session_state.data_baru_prestasi = pd.concat([st.session_state.data_baru_prestasi, 
                                                    entry], ignore_index=True) 
    #   refresh select box daftar sekolah
    with container_for_selectbox.container():
        sekolah_asal = st.selectbox("Sekolah Asal",daftar_sekolah[['sekolah_asal']])    
        id_daftar_sekolah = daftar_sekolah.loc[daftar_sekolah['sekolah_asal']==sekolah_asal,
                                               'id_daftar_sekolah'].iloc[0]    
        
    with container_for_optional_text.container():
        if sekolah_asal == "TIDAK TERDAFTAR": 
            sekolah_asal = st.text_input("Masukkan nama sekolah")       
            if submitted:
                df2 = pd.DataFrame([[daftar_sekolah.index[-1]+1,sekolah_asal,status_sekolah]], 
                                   columns=['id_daftar_sekolah','sekolah_asal','tipe_sekolah_asal'])
                daftar_sekolah = pd.concat([daftar_sekolah,df2], ignore_index=True)
                id_daftar_sekolah = daftar_sekolah.loc[daftar_sekolah['sekolah_asal']==sekolah_asal, 
                                                       'id_daftar_sekolah'].iloc[0]
                st.session_state.daftar_sekolah = daftar_sekolah

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
            retrain_ml(X_train, y_train, data_latih, regular_model)
