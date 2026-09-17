# DRAF PRD — Sistem Informasi Pengelolaan Stok Barang Berbasis Web dengan Random Forest

## 1. Ringkasan Eksekutif

**Sistem Informasi Pengelolaan Stok Barang Berbasis Web dengan Algoritma Random Forest** adalah sistem berbasis website yang membantu **Admin/Pengelola Stok CV. Bay Media** mencatat, memantau, dan melaporkan barang masuk, barang keluar, serta ketersediaan stok secara terstruktur.

Sistem dikembangkan untuk mengatasi pengelolaan stok yang masih dilakukan secara manual atau belum optimal, sehingga dapat terjadi kesalahan pencatatan, keterlambatan mengetahui kondisi stok, dan kesulitan memanfaatkan riwayat penjualan untuk memperkirakan kebutuhan barang pada periode berikutnya.

Selain digitalisasi pencatatan, produk memiliki satu fitur machine learning utama:

* **★ Random Forest Regression untuk Prediksi Kebutuhan Stok** — menggunakan data historis penjualan bulanan dan variabel pendukung yang tersedia untuk menghasilkan estimasi kebutuhan barang pada periode berikutnya.

Fokus prototype adalah membangun sistem yang dapat membuktikan bahwa pencatatan stok menjadi lebih terstruktur dan prediksi dapat membantu pengambilan keputusan pengadaan. Prediksi tidak melakukan pembelian otomatis; keputusan tetap dilakukan oleh pengguna yang berwenang.

---

# 2. Problem Statement & Bukti

## Problem Statement

CV. Bay Media menghadapi kendala dalam pengelolaan stok barang karena pencatatan dan pemantauan stok belum dilakukan secara terintegrasi. Pencatatan barang masuk dan barang keluar berpotensi mengalami kesalahan manusia, sedangkan informasi ketersediaan stok sulit dipantau secara cepat apabila data masih tersebar atau direkap secara manual.

Selain itu, riwayat penjualan yang telah tersedia belum dimanfaatkan secara optimal untuk memperkirakan kebutuhan stok pada periode berikutnya. Kondisi tersebut dapat menyulitkan pengelola dalam menentukan kebutuhan persediaan dan meningkatkan risiko stok terlalu sedikit atau terlalu banyak.

### Fakta/Permasalahan yang Menjadi Dasar Sistem

| No. | Permasalahan |
| --- | --- |
| 1 | Pencatatan barang masuk dan barang keluar belum terintegrasi dalam satu sistem. |
| 2 | Rekap transaksi stok berpotensi mengalami human error. |
| 3 | Informasi ketersediaan stok belum mudah dipantau secara real time. |
| 4 | Pembuatan laporan stok membutuhkan proses rekap data. |
| 5 | Riwayat penjualan belum dimanfaatkan secara optimal untuk memperkirakan kebutuhan stok periode berikutnya. |

### Asumsi

| ID | Asumsi |
| --- | --- |
| [ASUMSI-01] | Admin/Pengelola Stok menjadi pengguna utama dan bertanggung jawab terhadap validasi transaksi. |
| [ASUMSI-02] | Tersedia data historis penjualan bulanan yang cukup untuk membangun dan menguji model Random Forest Regression. |
| [ASUMSI-03] | Data historis memiliki periode waktu yang konsisten dan dapat diolah menjadi fitur model. |
| [ASUMSI-04] | Hasil prediksi digunakan sebagai informasi pendukung, bukan keputusan pembelian otomatis. |
| [ASUMSI-05] | Prototype tidak mencakup sistem akuntansi, kasir, supplier, atau pembelian otomatis secara penuh. |

---

# 3. Target User & Stakeholder

| Peran | Kebutuhan | Tingkat Pengaruh/Kepentingan |
| --- | --- | --- |
| **Admin/Pengelola Stok** | Mencatat barang, transaksi masuk/keluar, memantau stok, menjalankan prediksi, dan membuat laporan | **Tinggi / Tinggi** |
| **Pimpinan/Manajer** | Melihat kondisi stok, laporan, dan hasil prediksi kebutuhan barang | **Tinggi / Tinggi** |
| **Karyawan** | Menggunakan atau meminta barang sesuai proses internal perusahaan | **Sedang / Sedang** |

### Prioritas pengguna

**Primary user:** Admin/Pengelola Stok  
**Secondary user:** Pimpinan/Manajer  
**Operational stakeholder:** Karyawan

---

# 4. Value Proposition

## A. Pain yang Dikurangi

1. Mengurangi pencatatan stok secara manual.
2. Mengurangi risiko kesalahan ketika merekap barang masuk dan barang keluar.
3. Mempermudah pemantauan ketersediaan stok.
4. Mengurangi waktu pencarian data transaksi.
5. Mempermudah pembuatan laporan stok.
6. Mengurangi ketergantungan pada perkiraan manual dalam menentukan kebutuhan stok periode berikutnya.

## B. Gain yang Diciptakan

1. **Data stok terpusat** dan mudah ditelusuri.
2. **Informasi stok lebih cepat diperoleh** dari transaksi yang tersimpan.
3. **Laporan stok lebih mudah dibuat**.
4. **Prediksi kebutuhan barang** dapat diperoleh berdasarkan pola data historis.
5. **Pengambilan keputusan pengadaan lebih terinformasi** karena pengguna dapat mempertimbangkan hasil prediksi.

## C. Mengapa Random Forest Bukan Gimmick?

Random Forest ditempatkan pada aktivitas yang memang membutuhkan kemampuan prediksi, yaitu memperkirakan kebutuhan barang berdasarkan data historis penjualan.

Model menggunakan beberapa decision tree dan menggabungkan hasilnya untuk menghasilkan prediksi regresi. Pendekatan ini dipilih karena mampu menangani hubungan non-linear antarfitur dan dapat digunakan untuk memodelkan pola permintaan apabila data historis dan fitur yang digunakan memadai.

**Bottleneck yang diselesaikan:** sulit memperkirakan kebutuhan stok periode berikutnya hanya dari pemeriksaan stok saat ini.

> Hasil Random Forest merupakan rekomendasi berbasis data. Sistem tidak melakukan pembelian atau perubahan stok otomatis hanya berdasarkan prediksi.

---

# 5. Tujuan Produk & KPI Terukur

## Tujuan Produk

1. Mendigitalisasi pengelolaan stok barang CV. Bay Media.
2. Mengurangi kesalahan pencatatan transaksi stok.
3. Mempermudah pemantauan ketersediaan barang.
4. Mempercepat pencarian transaksi dan pembuatan laporan.
5. Mengimplementasikan Random Forest Regression untuk memprediksi kebutuhan stok periode berikutnya.
6. Menyediakan hasil prediksi sebagai informasi pendukung keputusan pengadaan.

## KPI

| Metric Utama | Target Prototype | Cara Mengukur |
| --- | ---: | --- |
| **Waktu pencatatan transaksi** | Turun ≥30% | Bandingkan waktu pencatatan manual dengan sistem |
| **Waktu pencarian data** | Turun ≥50% | Ukur waktu menemukan barang/transaksi tertentu |
| **Waktu pembuatan laporan** | Turun ≥50% | Bandingkan proses manual dan sistem |
| **Akurasi pencatatan stok** | ≥90% pada data uji | Bandingkan stok sistem dengan hasil pengecekan |
| **Kinerja prediksi** | Dievaluasi menggunakan MAE, RMSE, dan/atau MAPE | Bandingkan prediksi dengan nilai aktual pada data uji |
| **Keberhasilan proses prediksi** | ≥95% permintaan prediksi berhasil diproses | Hitung permintaan prediksi yang menghasilkan output valid |

**Catatan:** target operasional merupakan target prototype dan perlu disesuaikan dengan baseline aktual. Metrik akurasi model tidak ditetapkan secara arbitrer sebagai satu angka; hasil model dilaporkan berdasarkan metrik evaluasi yang sesuai dengan karakteristik data.

---

# 6. Scope Fitur 3 Bulan — MoSCoW

| Prioritas | Fitur | Deskripsi | Status |
| --- | --- | --- | --- |
| **Must Have** | Login & hak akses | Membatasi akses berdasarkan peran | Wajib |
| **Must Have** | Master data barang | CRUD data barang dan informasi stok | Wajib |
| **Must Have** | Barang masuk | Mencatat penambahan stok | Wajib |
| **Must Have** | Barang keluar | Mencatat pengurangan stok | Wajib |
| **Must Have** | Data penjualan bulanan | Menyimpan riwayat penjualan sebagai sumber prediksi | Wajib |
| **Must Have** | Random Forest Forecasting | Memprediksi kebutuhan stok periode berikutnya | Wajib ★ |
| **Must Have** | Dashboard stok | Menampilkan kondisi stok dan hasil prediksi | Wajib |
| **Must Have** | Laporan | Menampilkan riwayat dan rekap stok | Wajib |
| **Should Have** | Notifikasi stok minimum | Memberikan peringatan ketika stok mendekati batas yang ditentukan | Disarankan |
| **Should Have** | Filter laporan | Filter berdasarkan periode/barang | Disarankan |
| **Could Have** | Grafik tren penjualan | Visualisasi histori penjualan dan prediksi | Jika waktu cukup |
| **Could Have** | Ekspor laporan | Ekspor CSV/PDF | Jika waktu cukup |
| **Won't Have** | Pembelian otomatis | Sistem melakukan pembelian tanpa persetujuan pengguna | Di luar scope |
| **Won't Have** | Sistem kasir/keuangan | Pengelolaan keuangan perusahaan | Di luar scope |
| **Won't Have** | Integrasi supplier | Pemesanan langsung ke supplier | Di luar scope |

---

# 7. Intelligent Feature — Random Forest Regression

## Input

Data historis penjualan bulanan dan fitur yang tersedia, misalnya:

- periode/bulan;
- jumlah penjualan periode sebelumnya;
- lag penjualan beberapa periode;
- rata-rata penjualan historis;
- tren penjualan yang diturunkan dari data;
- fitur kalender yang relevan apabila tersedia.

## Proses

1. Data historis dikumpulkan dari transaksi penjualan.
2. Data dibersihkan dan divalidasi.
3. Data diubah menjadi fitur untuk supervised learning.
4. Data dibagi berdasarkan waktu menjadi data latih dan data uji agar tidak terjadi kebocoran informasi masa depan.
5. Model Random Forest Regression dilatih menggunakan data latih.
6. Model menghasilkan prediksi kebutuhan penjualan/stok periode berikutnya.
7. Hasil dievaluasi menggunakan MAE, RMSE, dan/atau MAPE sesuai kondisi data.
8. Hasil prediksi ditampilkan kepada pengguna sebagai informasi pendukung.

## Output

- estimasi kebutuhan barang periode berikutnya;
- nilai aktual dan prediksi pada periode pengujian;
- metrik evaluasi model;
- informasi pendukung keputusan pengadaan.

---

# 8. Batasan Produk

1. Sistem berbasis web.
2. Objek penelitian dibatasi pada pengelolaan stok barang di CV. Bay Media.
3. Random Forest digunakan untuk **regresi/prediksi kebutuhan stok**, bukan klasifikasi kondisi stok.
4. Prediksi menggunakan data historis penjualan bulanan yang tersedia.
5. Data transaksi yang digunakan harus melalui validasi sebelum menjadi dataset model.
6. Model tidak menjamin jumlah stok optimal secara mutlak; hasil bergantung pada kualitas dan jumlah data historis serta fitur yang digunakan.
7. Sistem tidak melakukan pembelian barang secara otomatis.
8. Analisis sentimen tidak termasuk dalam scope karena pilihan penelitian ini berfokus pada prediksi stok.
