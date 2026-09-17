# USER STORIES — Sistem Informasi Pengelolaan Stok dengan Random Forest

## Epik 1 — Login & Hak Akses

### US-01 — Login Pengguna
**Sebagai** pengguna terdaftar, **saya ingin** login ke sistem, **sehingga** saya dapat menggunakan fitur sesuai hak akses saya.

**Acceptance Criteria**
- Given pengguna memiliki akun valid, when memasukkan kredensial yang benar, then sistem mengizinkan masuk.
- Given kredensial salah, when login dilakukan, then sistem menolak akses dan menampilkan pesan yang sesuai.

### US-02 — Hak Akses
**Sebagai** Admin/Pengelola Stok, **saya ingin** hak akses diterapkan berdasarkan peran, **sehingga** hanya pengguna berwenang yang dapat mengubah data stok dan menjalankan proses model.

---

## Epik 2 — Master Data & Inventori

### US-03 — Master Barang
**Sebagai** Admin/Pengelola Stok, **saya ingin** mengelola data barang, **sehingga** setiap barang dapat dicatat dan dipantau secara terstruktur.

### US-04 — Transaksi Stok
**Sebagai** Admin/Pengelola Stok, **saya ingin** mencatat barang masuk dan barang keluar, **sehingga** saldo stok sistem dapat diperbarui berdasarkan transaksi.

**Acceptance Criteria**
- Given transaksi valid, when disimpan, then sistem menyimpan transaksi.
- Given barang masuk, when transaksi disimpan, then stok bertambah sesuai jumlah.
- Given barang keluar valid, when transaksi disimpan, then stok berkurang sesuai jumlah.
- Given barang keluar melebihi stok tersedia, when disimpan, then sistem menolak transaksi.

---

## Epik 3 — Monitoring & Laporan

### US-05 — Monitoring Stok
**Sebagai** Admin/Pimpinan, **saya ingin** melihat stok terkini dan riwayat transaksi, **sehingga** kondisi persediaan dapat dipantau dengan mudah.

### US-06 — Laporan
**Sebagai** Admin/Pimpinan, **saya ingin** melihat laporan stok dan transaksi berdasarkan periode, **sehingga** informasi dapat digunakan untuk evaluasi.

---

## Epik 4 — Data Penjualan

### US-07 — Riwayat Penjualan Bulanan
**Sebagai** Admin/Pengelola Stok, **saya ingin** menyimpan data penjualan bulanan, **sehingga** data tersebut dapat digunakan sebagai dasar forecasting.

**Acceptance Criteria**
- Data memiliki barang, periode, dan jumlah penjualan.
- Sistem menolak data dengan periode atau jumlah yang tidak valid.
- Data tersimpan dapat digunakan dalam proses pembentukan dataset.

---

## Epik 5 — Random Forest Forecasting ★

### US-08 — Prediksi Kebutuhan Stok
**Sebagai** Admin/Pengelola Stok, **saya ingin** sistem memprediksi kebutuhan barang menggunakan Random Forest Regression berdasarkan riwayat penjualan, **sehingga** saya memiliki informasi tambahan untuk menentukan kebutuhan stok periode berikutnya.

**Acceptance Criteria**
- Given data historis valid tersedia, when forecasting dijalankan, then sistem membentuk fitur dan menghasilkan prediksi numerik.
- Sistem tidak menggunakan data masa depan untuk memprediksi periode sebelumnya.
- Sistem menampilkan barang, periode prediksi, dan nilai prediksi.
- Jika data tidak mencukupi, sistem menampilkan informasi bahwa prediksi belum dapat dilakukan.

### US-09 — Evaluasi Model
**Sebagai** peneliti/Admin, **saya ingin** melihat MAE dan RMSE dari model, **sehingga** performa prediksi dapat dievaluasi secara objektif.

### US-10 — Peringatan Kebutuhan
**Sebagai** Admin/Pimpinan, **saya ingin** melihat indikator ketika hasil prediksi menunjukkan kebutuhan yang perlu diperhatikan, **sehingga** saya dapat mempertimbangkan tindakan pengadaan.

**Catatan:** indikator bukan perintah pembelian otomatis.
