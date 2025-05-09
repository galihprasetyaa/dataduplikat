
import streamlit as st
import pandas as pd

# Konfigurasi halaman
st.set_page_config(page_title="Cek Duplikat Data CSV", layout="wide")

# Header aplikasi
st.title("Deteksi Data Duplikat pada CSV")
st.markdown("Unggah file CSV Anda dan temukan baris yang duplikat berdasarkan seluruh atau sebagian kolom.")

# Upload file
uploaded_file = st.file_uploader("Pilih file CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Membaca file CSV
        try:
            df = pd.read_csv(uploaded_file)
        except UnicodeDecodeError:
            df = pd.read_csv(uploaded_file, encoding="latin1")

        st.subheader("Data Awal")
        st.write(f"Bentuk data: {df.shape}")
        st.dataframe(df.head())

        # Pilihan kolom untuk cek duplikat
        st.subheader("Deteksi Duplikat")
        st.markdown("Pilih kolom yang ingin Anda gunakan untuk mendeteksi duplikat. Biarkan kosong untuk menggunakan semua kolom.")

        selected_columns = st.multiselect("Kolom untuk deteksi duplikat", options=df.columns.tolist())

        # Cari duplikat
        if len(selected_columns) == 0:
            duplicates = df[df.duplicated(keep=False)]
        else:
            duplicates = df[df.duplicated(subset=selected_columns, keep=False)]

        st.write(f"Jumlah baris duplikat yang ditemukan: {duplicates.shape[0]}")
        if not duplicates.empty:
            st.dataframe(duplicates)
        else:
            st.success("Tidak ditemukan data duplikat.")

    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses file: {str(e)}")
else:
    st.info("Silakan unggah file CSV terlebih dahulu.")
