import cv2
import numpy as np
import streamlit as st

# --- 1. FUNGSI LOGIKA ASLI (DARI FILE KAMU) ---
def add_salt_pepper_noise(img, salt_prob=0.01, pepper_prob=0.01):
    noisy = img.copy()
    total_pixels = img.size
    # salt
    num_salt = int(total_pixels * salt_prob)
    coords = [np.random.randint(0, i-1, num_salt) for i in img.shape]
    noisy[coords[0], coords[1]] = 255
    # pepper
    num_pepper = int(total_pixels * pepper_prob)
    coords = [np.random.randint(0, i-1, num_pepper) for i in img.shape]
    noisy[coords[0], coords[1]] = 0
    return noisy

def mse(img1, img2):
    return np.mean((img1 - img2) ** 2)

def psnr(img1, img2):
    m = mse(img1, img2)
    if m == 0: return 100
    return 20 * np.log10(255.0 / np.sqrt(m))

# --- 2. KONFIGURASI HALAMAN DASHBOARD ---
st.set_page_config(page_title="Analisis Citra Satelit", layout="wide")
st.title("🛰️ Dashboard Analisis Median Filter & Canny Edge")
st.markdown("Dashboard ini digunakan untuk menganalisis pengaruh **Median Filtering** terhadap akurasi **Canny Edge Detection** pada citra satelit.")

# --- 3. SIDEBAR UNTUK INPUT ---
st.sidebar.header("Pengaturan Parameter")
uploaded_file = st.sidebar.file_uploader("Upload Citra Satelit", type=["png", "jpg", "jpeg"])
k_size = st.sidebar.select_slider("Pilih Ukuran Kernel Median Filter:", options=[3, 5, 7])
s_prob = st.sidebar.slider("Probabilitas Salt Noise:", 0.0, 0.05, 0.01)
p_prob = st.sidebar.slider("Probabilitas Pepper Noise:", 0.0, 0.05, 0.01)

if uploaded_file is not None:
    # Mengolah Gambar yang Diupload
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
    
    # Proses Utama
    noisy = add_salt_pepper_noise(image, s_prob, p_prob)
    median = cv2.medianBlur(noisy, k_size)
    edges = cv2.Canny(median, 100, 200)
    edges_no_filter = cv2.Canny(noisy, 100, 200)
    
    # Hitung Metrik
    mse_val = mse(image, median)
    psnr_val = psnr(image, median)
    edge_pixels = np.sum(edges == 255)
    edge_no_filter_pixels = np.sum(edges_no_filter == 255)

    # --- 4. TAMPILAN METRIK ---
    st.write("### 📊 Hasil Analisis Metrik")
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("MSE (Error)", f"{mse_val:.2f}")
    col_m2.metric("PSNR (Kualitas)", f"{psnr_val:.2f} dB")
    col_m3.metric("Edge Pixels (Filtered)", f"{edge_pixels}")

    # --- 5. TAMPILAN GAMBAR ---
    st.write("---")
    row1 = st.columns(3)
    row1[0].image(image, caption="1. Citra Asli (Grayscale)")
    row1[1].image(noisy, caption="2. Citra + Salt & Pepper Noise")
    row1[2].image(edges_no_filter, caption=f"3. Canny Tanpa Filter (Edge: {edge_no_filter_pixels})")

    st.write("---")
    row2 = st.columns(2)
    row2[0].image(median, caption=f"4. Hasil Median Filter (Kernel {k_size})")
    row2[1].image(edges, caption=f"5. Hasil Canny Setelah Filter (Kernel {k_size})")

    # --- 6. KESIMPULAN OTOMATIS (VERSI OMNI-ANALYSIS) ---
    st.sidebar.write("---")
    st.sidebar.subheader("💡 Analisis Sistem Cerdas")
    
    # 1. Menghitung Statistik Perbaikan
    # Mencegah pembagian dengan nol jika gambar sangat bersih
    if edge_no_filter_pixels > 0:
        reduksi_noise = ((edge_no_filter_pixels - edge_pixels) / edge_no_filter_pixels) * 100
    else:
        reduksi_noise = 0

    # 2. Logika Penentuan Tingkat Gangguan (Noise)
    total_noise_prob = s_prob + p_prob
    if total_noise_prob <= 0.02:
        level_gangguan = "Rendah"
    elif total_noise_prob <= 0.07:
        level_gangguan = "Sedang"
    else:
        level_gangguan = "Tinggi (Ekstrem)"

    # 3. Logika Penilaian Kualitas (PSNR)
    if psnr_val >= 30:
        kualitas_status = "Sangat Bagus (Detail Terjaga)"
    elif psnr_val >= 26:
        kualitas_status = "Optimal (Keseimbangan Baik)"
    else:
        kualitas_status = "Kurang (Terlalu Blur atau Terlalu Kotor)"

    # 4. Logika Saran Teknis Gabungan (Kernel + Noise)
    if total_noise_prob > 0.06 and k_size == 3:
        saran = "⚠️ Noise terlalu padat untuk Kernel 3. Hasil Canny masih kotor. Disarankan naik ke Kernel 5."
    elif total_noise_prob < 0.03 and k_size > 3:
        saran = "⚠️ Noise cukup rendah. Kernel besar membuat gambar terlalu blur. Disarankan turun ke Kernel 3 untuk menjaga detail."
    elif k_size == 3 and psnr_val >= 30:
        saran = "✅ Ini adalah konfigurasi paling ideal untuk citra satelit ini."
    else:
        saran = "ℹ️ Konfigurasi sudah cukup baik dalam menangani karakteristik noise saat ini."

    # 5. Menampilkan Output ke Sidebar
    kesimpulan_html = f"""
    **Kondisi Data:**
    * Tingkat Noise: `{level_gangguan}`
    * Reduksi Deteksi Palsu: `{reduksi_noise:.1f}%`

    **Performa Filter:**
    * Status: **{kualitas_status}**
    * Akurasi MSE: `{mse_val:.2f}`

    **Rekomendasi Ahli:**
    _{saran}_
    """
    
    st.sidebar.info(kesimpulan_html)