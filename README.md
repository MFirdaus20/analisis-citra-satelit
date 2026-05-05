# 🛰️ Satellite Image Analysis Dashboard

Dashboard interaktif berbasis web untuk menganalisis pengaruh **Median Filtering** terhadap akurasi **Canny Edge Detection** pada citra satelit yang terkena noise _Salt & Pepper_.

## 📋 Deskripsi Proyek

Proyek ini dikembangkan untuk memvisualisasikan bagaimana pemrosesan citra digital dapat membantu mengekstraksi informasi penting (garis tepi/edge) dari gambar satelit yang terdistorsi. Dashboard ini memungkinkan pengguna untuk melakukan eksperimen secara _real-time_ dengan berbagai parameter.

## 🚀 Fitur Utama

- **Dynamic Noise Injection**: Menambahkan noise _Salt & Pepper_ dengan probabilitas yang bisa diatur.
- **Interactive Filtering**: Mengubah ukuran kernel Median Filter (3, 5, atau 7) secara instan.
- **Automated Metrics**: Perhitungan otomatis nilai **MSE** (Mean Squared Error) dan **PSNR** (Peak Signal-to-Noise Ratio).
- **Smart Conclusion**: Sistem memberikan rekomendasi otomatis berdasarkan hasil analisis data.

## 🛠️ Teknologi yang Digunakan

- **Python**: Bahasa pemrograman utama.
- **Streamlit**: Framework untuk membangun dashboard web.
- **OpenCV**: Library utama untuk pengolahan citra (Filtering & Canny Edge).
- **NumPy**: Untuk pengolahan matriks dan perhitungan metrik.

## 📦 Cara Menjalankan Secara Lokal

1. Clone repositori ini:
   ```bash
   git clone [https://github.com/MFirdaus20/analisis-citra-satelit.git](https://github.com/MFirdaus20/analisis-citra-satelit.git)

   ```

2. Masuk ke direktori proyek:
   ```bash
   cd analisis-citra-satelit

   ```

3. Install library yang dibutuhkan:
   ```bash
   pip install -r requirements.txt

   ```

4. Jalankan aplikasi:
   ```bash
   streamlit run citra_satelit.py

   ```

5. ## 📊 Hasil Analisis
   Berdasarkan pengujian, **Kernel 3** seringkali menjadi titik optimal untuk menjaga detail citra satelit, sementara **Kernel 7** lebih efektif untuk noise yang sangat padat namun memberikan efek _blur_ yang lebih tinggi.
