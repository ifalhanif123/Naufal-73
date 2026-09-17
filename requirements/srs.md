# SOFTWARE REQUIREMENTS SPECIFICATION (SRS)
## Sistem Informasi Pengelolaan Stok Barang Berbasis Web dengan Algoritma Random Forest

## 1. Pendahuluan

### 1.1 Tujuan

SRS ini mendefinisikan kebutuhan fungsional, non-fungsional, aturan bisnis, kebutuhan data, dan batasan sistem untuk aplikasi pengelolaan stok barang berbasis web pada CV. Bay Media dengan fitur prediksi kebutuhan stok menggunakan Random Forest Regression.

### 1.2 Ruang Lingkup

Sistem mencakup autentikasi, master barang, transaksi barang masuk, transaksi barang keluar, data penjualan bulanan, pemantauan stok, forecasting Random Forest, dashboard, dan laporan.

---

# 2. Functional Requirements

| ID | Functional Requirement | Prioritas |
| --- | --- | --- |
| **FR-01** | Sistem harus menyediakan autentikasi pengguna. | Must Have |
| **FR-02** | Sistem harus menerapkan hak akses berdasarkan peran pengguna. | Must Have |
| **FR-03** | Sistem harus dapat menambah, mengubah, melihat, dan menghapus data barang sesuai hak akses. | Must Have |
| **FR-04** | Sistem harus dapat mencatat transaksi barang masuk. | Must Have |
| **FR-05** | Sistem harus dapat mencatat transaksi barang keluar. | Must Have |
| **FR-06** | Sistem harus memperbarui saldo stok berdasarkan transaksi yang tervalidasi. | Must Have |
| **FR-07** | Sistem harus menampilkan ketersediaan stok barang. | Must Have |
| **FR-08** | Sistem harus menyimpan riwayat transaksi stok. | Must Have |
| **FR-09** | Sistem harus menyediakan pencatatan data penjualan berdasarkan periode bulanan. | Must Have |
| **FR-10** | Sistem harus menyediakan pencarian dan filter data barang/transaksi. | Should Have |
| **FR-11** | Sistem harus menyediakan laporan stok dan transaksi. | Must Have |
| **FR-12** | Sistem harus menyediakan dashboard ringkasan kondisi stok. | Must Have |
| **FR-13** | Sistem harus memvalidasi data sebelum digunakan sebagai input model. | Must Have |
| **FR-14** | Sistem harus membentuk fitur historis dari data penjualan untuk proses forecasting. | Must Have |
| **FR-15** | Sistem harus dapat melatih Random Forest Regression menggunakan dataset yang telah disiapkan. | Must Have ★ |
| **FR-16** | Sistem harus dapat menghasilkan prediksi kebutuhan barang untuk periode berikutnya. | Must Have ★ |
| **FR-17** | Sistem harus menampilkan hasil prediksi beserta periode dan barang yang diprediksi. | Must Have ★ |
| **FR-18** | Sistem harus menyediakan metrik evaluasi model pada proses pengujian. | Must Have |
| **FR-19** | Sistem harus menampilkan informasi peringatan apabila hasil prediksi menunjukkan kebutuhan yang perlu diperhatikan. | Should Have |
| **FR-20** | Sistem harus menyediakan grafik tren historis dan prediksi jika fitur visualisasi diaktifkan. | Could Have |
| **FR-21** | Sistem harus dapat mencatat waktu dan pengguna yang menjalankan proses prediksi. | Should Have |
| **FR-22** | Sistem tidak boleh mengubah stok fisik atau melakukan pembelian otomatis hanya berdasarkan hasil prediksi. | Must Have |

---

# 3. Non-Functional Requirements

| ID | Kategori | Requirement | Target |
| --- | --- | --- | --- |
| **NFR-01** | Usability | Antarmuka dapat digunakan Admin untuk pencatatan stok tanpa proses yang tidak perlu. | Lulus uji pengguna |
| **NFR-02** | Performance | Halaman transaksi umum harus merespons secara wajar pada lingkungan prototype. | ≤3 detik untuk operasi normal* |
| **NFR-03** | Performance | Proses prediksi harus memberikan hasil atau pesan kegagalan yang jelas. | ≤10 detik pada dataset prototype* |
| **NFR-04** | Security | Password tidak disimpan dalam bentuk plaintext. | Wajib |
| **NFR-05** | Security | Fitur pengelolaan stok dan model hanya dapat diakses pengguna berwenang. | Wajib |
| **NFR-06** | Reliability | Transaksi tervalidasi tidak boleh menggandakan perubahan stok akibat satu submit. | 100% pada test case |
| **NFR-07** | Data Integrity | Stok sistem harus konsisten dengan transaksi yang tersimpan. | ≥90% pada pengujian prototype |
| **NFR-08** | Maintainability | Struktur kode memisahkan komponen aplikasi, data, dan proses model sejauh memungkinkan. | Wajib |
| **NFR-09** | Compatibility | Sistem dapat dijalankan melalui browser modern pada perangkat desktop/laptop. | Wajib |

*Target performa merupakan target prototype dan perlu divalidasi pada lingkungan implementasi sebenarnya.

---

# 4. Business Rules

| ID | Business Rule |
| --- | --- |
| **BR-01** | Setiap barang memiliki identitas unik. |
| **BR-02** | Barang masuk menambah stok. |
| **BR-03** | Barang keluar mengurangi stok. |
| **BR-04** | Stok tidak boleh menjadi negatif melalui transaksi yang tidak valid. |
| **BR-05** | Setiap transaksi harus memiliki tanggal/periode dan jumlah barang. |
| **BR-06** | Data penjualan yang digunakan model harus melewati validasi. |
| **BR-07** | Pembagian data training dan testing harus mempertahankan urutan waktu untuk data forecasting. |
| **BR-08** | Data masa depan tidak boleh digunakan sebagai fitur untuk memprediksi periode sebelumnya. |
| **BR-09** | Hasil prediksi merupakan estimasi dan tidak otomatis mengubah stok. |
| **BR-10** | Keputusan pengadaan tetap berada pada pengguna yang berwenang. |
| **BR-11** | Metrik evaluasi model harus dihitung dari data uji yang tidak digunakan untuk melatih model. |
| **BR-12** | Jika data tidak mencukupi atau tidak valid, sistem harus memberi informasi dan tidak memaksakan prediksi. |

---

# 5. Data Requirements

### Entitas utama

- **User**: identitas dan hak akses pengguna.
- **Barang**: kode, nama, satuan, stok, dan informasi dasar barang.
- **BarangMasuk**: tanggal, barang, jumlah, dan keterangan.
- **BarangKeluar**: tanggal, barang, jumlah, dan keterangan.
- **PenjualanBulanan**: barang, bulan, tahun, dan jumlah penjualan.
- **Prediksi**: barang, periode prediksi, nilai prediksi, model, dan waktu proses.
- **EvaluasiModel**: periode/data uji, MAE, RMSE, MAPE bila valid, dan informasi model.

---

# 6. Kebutuhan Model Random Forest

### 6.1 Jenis Model

**Random Forest Regression**.

### 6.2 Target Prediksi

Jumlah kebutuhan/permintaan barang pada periode berikutnya berdasarkan data historis penjualan.

### 6.3 Contoh Pembentukan Dataset

| Bulan | Penjualan t-3 | Penjualan t-2 | Penjualan t-1 | Rata-rata Historis | Target t |
| --- | ---: | ---: | ---: | ---: | ---: |
| Apr | 10 | 12 | 15 | 12,33 | 18 |
| Mei | 12 | 15 | 18 | 15,00 | 16 |
| Jun | 15 | 18 | 16 | 16,33 | 20 |

Contoh tersebut hanya ilustrasi. Dataset penelitian harus menggunakan data aktual yang tersedia dan skema fitur yang ditetapkan setelah eksplorasi data.

### 6.4 Evaluasi

Model diuji menggunakan data yang dipisahkan berdasarkan waktu. Metrik yang dapat digunakan:

- **MAE (Mean Absolute Error)** untuk rata-rata kesalahan absolut;
- **RMSE (Root Mean Squared Error)** untuk memberi penalti lebih besar pada kesalahan besar;
- **MAPE (Mean Absolute Percentage Error)** jika nilai aktual tidak mengandung nol atau ditangani dengan metode yang sesuai.

### 6.5 Quality Gate Forecasting

| Parameter | Target/Kriteria |
| --- | --- |
| Data historis | Valid dan memiliki periode yang cukup untuk pembentukan fitur |
| Data leakage | Tidak terjadi |
| Training/testing | Dipisahkan berdasarkan waktu |
| Output | Prediksi numerik untuk periode berikutnya |
| Evaluasi | Minimal MAE dan RMSE; MAPE bila sesuai |
| Interpretasi | Hasil dipahami sebagai estimasi, bukan kepastian |
| Pengubahan stok | Tidak otomatis berdasarkan prediksi |

---

# 7. Traceability Ringkas

**US-01 → FR-01 & FR-02**  
**US-02 → FR-03, FR-04, FR-05 & FR-06**  
**US-03 → FR-07, FR-08 & FR-11**  
**US-04 → FR-09 & FR-13**  
**US-05 → FR-14 & FR-15**  
**US-06 → FR-16 & FR-17**  
**US-07 → FR-18**  
**US-08 → FR-19 & FR-22**
