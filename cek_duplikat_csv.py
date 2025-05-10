import streamlit as st
import pandas as pd

# Konfigurasi halaman
st.set_page_config(page_title="Cek Duplikat per Kolom", layout="wide")

# Header aplikasi
st.title("🔍 Deteksi Nilai Duplikat pada Kolom CSV")
st.markdown("Unggah file CSV dan pilih kolom untuk mendeteksi nilai yang muncul lebih dari satu kali.")

# Upload file
uploaded_file = st.file_uploader("📁 Unggah file CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Membaca file CSV
        try:
            df = pd.read_csv(uploaded_file)
        except UnicodeDecodeError:
            df = pd.read_csv(uploaded_file, encoding="latin1")

        st.subheader("📋 Pratinjau Data")
        st.write(f"Ukuran data: {df.shape}")
        st.dataframe(df.head())

        # Pilih kolom untuk cek duplikat
        st.subheader("🔁 Pilih Kolom untuk Pengecekan Duplikat")
        selected_column = st.selectbox("Pilih satu kolom", df.columns.tolist())

        if selected_column:
            duplicated_values = df[selected_column][df[selected_column].duplicated(keep=False)]
            result_df = df[df[selected_column].isin(duplicated_values)]

            count_duplicates = duplicated_values.value_counts()

            st.write(f"Jumlah nilai duplikat yang ditemukan: {len(count_duplicates)}")
            if not result_df.empty:
                st.subheader("📑 Baris dengan Nilai Duplikat")
                st.dataframe(result_df)

                st.subheader("📈 Ringkasan Jumlah Duplikat")
                st.dataframe(count_duplicates.reset_index().rename(columns={
                    "index": selected_column,
                    selected_column: "Jumlah Kemunculan"
                }))

                # Export hasil
                csv = result_df.to_csv(index=False).encode("utf-8")
                st.download_button("⬇️ Unduh Baris Duplikat", csv, "baris_duplikat.csv", "text/csv")
            else:
                st.success("Tidak ada nilai duplikat di kolom yang dipilih.")

    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {str(e)}")
else:
    st.info("Silakan unggah file CSV terlebih dahulu.")
