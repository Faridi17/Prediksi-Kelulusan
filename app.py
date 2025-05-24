import joblib
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import streamlit as st
import numpy as np

# Load model
model = joblib.load('decision_tree_model.pkl')

# Form input
st.title("Klasifikasi Kelulusan Mahasiswa (Tepat / Terlambat)")

jenis_kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
umur = st.number_input("Umur", min_value=17, max_value=50)
status_mahasiswa = st.selectbox("Status Mahasiswa", ["Mahasiswa", "Bekerja"])
status_nikah = st.selectbox("Status Nikah", ["Menikah", "Belum Menikah"])

ips_values = []
for i in range(1, 9):
    ips = st.number_input(f"IPS{i}", min_value=0.0, max_value=4.0, step=0.01)
    ips_values.append(ips)

ipk = st.number_input("IPK", min_value=0.0, max_value=4.0, step=0.01)

if st.button("Klasifikasikan"):
    # Preprocessing input (harus sesuai urutan saat training)
    jenis_kelamin_encoded = 1 if jenis_kelamin == "Laki-laki" else 0
    status_mahasiswa_encoded = 1 if status_mahasiswa == "Mahasiswa" else 0
    status_nikah_encoded = 1 if status_nikah == "Menikah" else 0

    input_data = [
        jenis_kelamin_encoded,
        status_mahasiswa_encoded,
        umur,
        status_nikah_encoded
    ] + ips_values + [ipk]

    st.write("Jumlah fitur input:", len(input_data))  # Harus cocok dgn fitur saat training

    try:
        prediction = model.predict([input_data])
        hasil = prediction[0]

        # Jika hasil prediksi dalam bentuk angka, ubah dulu ke label
        label_map = {0: "Terlambat", 1: "Tepat"}  # Sesuaikan dengan modelmu
        if isinstance(hasil, (int, np.integer)):
            hasil = label_map.get(hasil, str(hasil))

        # Tampilkan dengan warna
        if hasil.lower() == "tepat":
            st.markdown(f"<h4 style='color:green;'>Hasil Prediksi: {hasil}</h4>", unsafe_allow_html=True)
        elif hasil.lower() == "terlambat":
            st.markdown(f"<h4 style='color:red;'>Hasil Prediksi: {hasil}</h4>", unsafe_allow_html=True)
        else:
            st.warning(f"Hasil Prediksi: {hasil}")

    except Exception as e:
        st.error(f"Gagal memproses prediksi: {e}")
