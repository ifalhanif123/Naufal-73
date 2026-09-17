# USE CASE DETAIL — Random Forest Forecasting Kebutuhan Stok

## 1. Identitas Use Case

| Elemen | Detail |
| --- | --- |
| **Use Case** | **UC-01 — Random Forest Forecasting Kebutuhan Stok** |
| **Aktor Utama** | **Admin/Pengelola Stok** |
| **Aktor Sekunder** | **Pimpinan/Manajer** |
| **Deskripsi Ringkas** | Use case ini memungkinkan Admin mengolah data historis penjualan, menjalankan Random Forest Regression, memperoleh prediksi kebutuhan barang periode berikutnya, melihat metrik evaluasi, dan menggunakan hasilnya sebagai informasi pendukung keputusan stok. |
| **FR Terkait** | FR-09, FR-13, FR-14, FR-15, FR-16, FR-17, FR-18, FR-19, FR-22 |
| **NFR Terkait** | NFR-03, NFR-05, NFR-07, NFR-08 |
| **BR Terkait** | BR-06, BR-07, BR-08, BR-09, BR-11, BR-12 |
| **Prioritas** | **Must Have ★** |

### Pre-kondisi

1. Admin telah login.
2. Admin memiliki hak akses forecasting.
3. Data penjualan historis tersedia dan telah divalidasi.
4. Dataset memiliki periode yang cukup untuk pembentukan fitur.
5. Parameter model dan skema fitur telah ditentukan pada implementasi.

### Post-kondisi

Jika berhasil:

1. Sistem menghasilkan prediksi numerik kebutuhan barang periode berikutnya.
2. Sistem menyimpan hasil prediksi dan waktu proses.
3. Sistem menampilkan hasil prediksi kepada pengguna.
4. Jika proses evaluasi dilakukan, sistem menampilkan metrik model.
5. Prediksi tidak otomatis mengubah stok atau melakukan pembelian.

---

## 2. Skenario Utama — Happy Flow

1. **Aktor:** Admin memilih menu Forecasting.
2. **Sistem:** Sistem menampilkan pilihan barang/periode dan data historis yang tersedia.
3. **Aktor:** Admin memilih data/periode yang akan digunakan.
4. **Sistem:** Sistem memvalidasi kelengkapan dan konsistensi data.
5. **Sistem:** Sistem membentuk fitur historis, seperti lag dan statistik historis sesuai rancangan model.
6. **Sistem:** Sistem membagi data latih dan data uji berdasarkan urutan waktu.
7. **Sistem:** Sistem melatih Random Forest Regression menggunakan data latih.
8. **Sistem:** Sistem melakukan prediksi pada data uji dan/atau periode berikutnya.
9. **Sistem:** Sistem menghitung metrik evaluasi yang dipilih pada data uji.
10. **Sistem:** Sistem menghasilkan estimasi kebutuhan barang periode berikutnya.
11. **Sistem:** Sistem menampilkan barang, periode, prediksi, dan informasi evaluasi yang relevan.
12. **Aktor:** Admin/Pimpinan menggunakan informasi tersebut sebagai bahan pertimbangan pengadaan.
13. **Sistem:** Sistem menyimpan riwayat proses prediksi.

---

## 3. Skenario Alternatif / Pengecualian

### AF-01 — Data Tidak Mencukupi

1. Admin menjalankan forecasting.
2. Sistem memeriksa data historis.
3. Sistem menemukan jumlah data tidak mencukupi untuk fitur yang dibutuhkan.
4. Sistem tidak menjalankan prediksi final.
5. Sistem menampilkan pesan bahwa data perlu dilengkapi.

### AF-02 — Data Tidak Valid

1. Sistem menemukan nilai kosong, duplikat periode, atau nilai penjualan yang tidak valid.
2. Sistem menandai data bermasalah.
3. Sistem tidak memasukkan data bermasalah ke dataset model sampai diperbaiki.
4. Admin memperbaiki data.
5. Forecasting dapat dijalankan kembali.

### AF-03 — Risiko Data Leakage

1. Sistem membentuk dataset forecasting.
2. Sistem memeriksa fitur dan target.
3. Jika fitur menggunakan informasi dari periode setelah target, sistem harus menolak konfigurasi tersebut atau memperbaikinya sebelum training.
4. Model hanya dijalankan setelah urutan waktu valid.

### AF-04 — Proses Model Gagal

1. Admin menjalankan forecasting.
2. Sistem gagal melatih atau menjalankan model.
3. Sistem menampilkan pesan kesalahan yang tidak membingungkan pengguna.
4. Sistem tidak menyimpan prediksi yang tidak valid sebagai hasil final.

### AF-05 — Prediksi Menunjukkan Kebutuhan Tinggi

1. Sistem menghasilkan prediksi kebutuhan yang lebih tinggi dari batas internal yang telah ditentukan.
2. Sistem memberikan indikator/peringatan.
3. Admin memeriksa stok aktual dan hasil prediksi.
4. Keputusan pengadaan dilakukan oleh pengguna berwenang.
5. Sistem tidak melakukan pembelian otomatis.

---

# 4. Acceptance Criteria

## Skenario 1 — Forecasting Berhasil

**Given**

* Admin telah login dan memiliki akses forecasting.
* Data historis penjualan valid dan cukup.
* Fitur historis dapat dibentuk.

**When**

* Admin menjalankan Random Forest Regression.

**Then**

* Sistem memvalidasi dataset.
* Sistem memisahkan data training dan testing berdasarkan waktu.
* Sistem menghasilkan prediksi numerik.
* Sistem menampilkan barang dan periode prediksi.
* Sistem menyimpan hasil proses.

**Status yang diharapkan:** **PASS**

---

## Skenario 2 — Data Tidak Cukup

**Given**

* Admin memiliki akses forecasting.
* Data historis tidak memenuhi jumlah minimum yang dibutuhkan untuk fitur model.

**When**

* Admin menjalankan forecasting.

**Then**

* Sistem tidak menghasilkan prediksi final.
* Sistem menampilkan informasi bahwa data perlu dilengkapi.
* Sistem tidak menyimpan hasil prediksi yang tidak valid.

**Status yang diharapkan:** **PASS**

---

## Skenario 3 — Evaluasi Model

**Given**

* Data training dan testing telah dipisahkan berdasarkan waktu.
* Model berhasil menghasilkan prediksi pada data testing.

**When**

* Sistem menjalankan evaluasi.

**Then**

* Sistem menghitung minimal MAE dan RMSE.
* Nilai metrik ditampilkan atau disimpan untuk dokumentasi penelitian.
* Data testing tidak digunakan untuk melatih model pada proses evaluasi yang sama.

**Status yang diharapkan:** **PASS**

---

## Skenario 4 — Tidak Ada Pembelian Otomatis

**Given**

* Sistem telah menghasilkan prediksi kebutuhan stok.

**When**

* Prediksi menunjukkan kebutuhan tinggi.

**Then**

* Sistem dapat memberikan indikator/peringatan.
* Sistem tidak membuat transaksi pembelian otomatis.
* Pengguna berwenang tetap melakukan keputusan.

**Status yang diharapkan:** **PASS**

---

# 5. Quality Gate Use Case

| Parameter | Target | Hasil yang Dinyatakan Lulus |
| --- | ---: | --- |
| **Kelengkapan data** | Sesuai kebutuhan fitur | Dataset dapat diproses tanpa field wajib yang hilang |
| **Data leakage** | Tidak ada | Tidak ada informasi masa depan pada fitur prediksi |
| **Pemisahan data** | Berdasarkan waktu | Training mendahului testing secara kronologis |
| **Output prediksi** | Numerik | Nilai prediksi berhasil dihasilkan |
| **Evaluasi** | Minimal MAE + RMSE | Kedua metrik dapat dihitung pada data uji |
| **Latensi prototype** | ≤10 detik* | Hasil/pesan proses tersedia dalam batas target pada dataset prototype |
| **Integritas stok** | Tidak berubah otomatis | Forecasting tidak mengubah saldo stok |
| **Keputusan pengadaan** | Oleh pengguna | Sistem hanya memberikan informasi/indikator |

*Target performa perlu divalidasi pada lingkungan implementasi dan ukuran dataset sebenarnya.

---

# 6. Traceability

**US-07 → FR-09 & FR-13 → BR-06 → UC-01**  
**US-08 → FR-14, FR-15, FR-16 & FR-17 → BR-07, BR-08 & BR-09 → UC-01**  
**US-09 → FR-18 → BR-11 → UC-01**  
**US-10 → FR-19 & FR-22 → BR-10 → UC-01**

Dengan demikian, UC-01 mencakup alur utama implementasi Random Forest Regression untuk prediksi kebutuhan stok tanpa masuk ke ranah desain UI, UML, arsitektur teknis, atau struktur database secara mendalam.
