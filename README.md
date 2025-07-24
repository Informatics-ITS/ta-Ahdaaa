# 🏁 Tugas Akhir (TA) - Final Project

- **Nama Mahasiswa**: Ahda Filza Ghaffaru
- **NRP**: 5025211144
- **Judul TA**: STUDI PERBANDINGAN PRINCIPAL COMPONENT ANALYSIS (PCA) dan t-DISTRIBUTED STOCHASTIC NEIGHBOR EMBEDDING (t-SNE) DALAM DETEKSI CACAT PERANGKAT LUNAK 
- **Dosen Pembimbing**: Ir. Siti Rochimah, MT., Ph.D 
- **Dosen Ko-pembimbing**: Dini Adni Navastara, S.Kom, M.Sc.

---

## 📺 Demo Aplikasi

Embed video demo di bawah ini:

[Demo Aplikasi](https://www.youtube.com/watch?v=VIDEO_ID)  
_Klik tulisan di atas untuk menonton demo_

---

## 🛠 Panduan Instalasi & Menjalankan Folder `Comparison-PCA-TSNE`

### Prasyarat

- Daftar dependensi (contoh):
  - Python 3.10 (wajib, untuk kompatibilitas dengan seluruh pustaka yang digunakan)
  - pip (Python package installer)
  - Git
    
### Langkah-langkah

1. **Clone Repository**
   ```bash
   git clone https://github.com/Informatics-ITS/ta-Ahdaaa
   ```
2. **Siapkan Cleaned D'' Dataset NASA MDP**

- Unduh seluruh dataset dari [sini](https://github.com/klainfo/NASADefectDataset).
- Masukkan semua file .arff ke dalam folder /Comparison-PCA-TSNE/data

3. **Clone Parametric t-SNE**
   Pastikan Anda sudah meng-pull repositori parametric t-SNE dari jsilter, karena ini digunakan dalam analisis:

   ```bash
   git clone https://github.com/jsilter/parametric_tsne.git
   ```

4. **Instalasi Dependensi**
   Pastikan Anda berada di dalam folder Comparison-PCA-TSNE, lalu jalankan:

   ```bash
   pip install -r requirements_310.txt
   ```

5. **Jalankan Aplikasi**
   Tidak perlu menjalankan main.py atau API. Cukup buka dan jalankan notebook Jupyter. Untuk analisis gabungan jalankan

   ```bash
   /Comparison-PCA-TSNE/notebooks/analysis.ipynb
   ```

   Sementara untuk analisis terpisah, jalankan separate.ipynb dengan mengisi variabel `dataset_name`

## 🛠 Panduan Instalasi & Menjalankan Folder `Model-Test-Web`

Antarmuka web ini dibangun menggunakan **Vue.js** dan digunakan untuk:

- Mengunggah file Python untuk diprediksi oleh model
- Mengunggah file JSON berisi metrik kompleksitas
- Menampilkan hasil prediksi dan evaluasi model secara visual

### Prasyarat

- Daftar dependensi (contoh):
  - Python 3.10+
  - pip (Python package installer)
  - Git
  - [Node.js](https://nodejs.org/) (versi 16.x atau 18.x direkomendasikan)
  - npm (biasanya sudah satu paket dengan Node.js)

### Langkah-langkah Backend

1. **Clone Repository**
   ```bash
   git clone https://github.com/Informatics-ITS/ta-Ahdaaa
   ```
2. **Unduh Model Terbaik**

- Unduh file model .pkl dari link [berikut](https://drive.google.com/file/d/1M5nnmA2XwW22x2Buzb6DR8TEjiMOaVh8/view?usp=sharing)
- Lalu, letakkan file tersebut di dalam folder berikut: `/Model-Test-Web/backend/Model`

3. **Instalasi Dependensi**
   Pastikan Anda berada di dalam folder `/Model-Test-Web/backend/`, lalu jalankan:

   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan Aplikasi**

   ```bash
   uvicorn main:app --reload
   ```

### Langkah-langkah Backend

1. **Instalasi Dependensi**
   Pastikan Anda berada di dalam folder `/Model-Test-Web/frontend/`, lalu jalankan:

   ```bash
   npm install
   ```

2. **Jalankan Aplikasi**

   ```bash
   npm run dev
   ```

3. **Buka Browser**

   ```bash
   http://localhost:5173
   ```

   Jika port berbeda (misalnya karena konflik), terminal akan menampilkan port baru.

---

## 📚 Dokumentasi Tambahan

- [Hasil Excel Perbandingan Seluruh Skenario](https://docs.google.com/spreadsheets/d/1Qh_lZc0b3mlPFUS0Zy01gvwzgw8URfgS/edit?usp=sharing&ouid=107222116685887205627&rtpof=true&sd=true)

---

## ⁉️ Pertanyaan?

Hubungi:

- Penulis: [5025211144@student.its.ac.id]
- Pembimbing Utama: [siti@if.its.ac.id]
