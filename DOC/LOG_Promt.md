[Peran] 
Kamu adalah Software Architect Senior untuk aplikasi Web berfitur AI.

[Tugas] 
Buat DRAF High-Level Design (HLD) berdasarkan PRD, SRS, dan User Stories dari "Smart Inventory & Stock Demand Forecasting System" yang dilampirkan di bawah ini.

[Konteks & Ringkasan Acuan]
--------------------------------------------------------------------------------
1. Platform & Stack Teknology:
   - Frontend: Web Platform (HTML5, Bootstrap/Tailwind CSS, JavaScript/Blade)
   - Backend API: PHP Framework (Laravel / CodeIgniter 4)
   - Database: MySQL
   - AI Engine/Service: Python Service (FastAPI / Flask) atau External Cloud AI API (Tesseract/Google Vision & Scikit-Learn/Statsmodels)

2. Konstrain & Batasan Ringkas:
   - Durasi Pengerjaan: Prototype MVP 1 Semester (3–4 bulan).
   - Anggaran & Resource AI: Terbatas (fokus pada arsitektur modular, efisien, dan biaya minimal).
   - Fitur AI Inti (★ Must Have):
     a) AI OCR & Intelligent Document Parsing (FR-14, FR-15, FR-16 | US-15, US-16, US-17)
     b) AI Stock Demand Forecasting & Auto-Reorder Point (FR-11, FR-12, FR-13 | US-18, US-19, US-20)
   - Non-Functional Target (NFR):
     * Akurasi OCR ≥80%, Akurasi Forecasting/Deteksi Stok Kritis ≥80%.
     * Latensi Pemrosesan AI ≤10 detik/transaksi (NFR-07).
     * Keamanan: Autentikasi berbasis Sesi/JWT, Isolasai Hak Akses (RBAC), Enkripsi Kredensial.
     * Privasi & Validasi: Data AI diproses hanya untuk inventori (NFR-11) & WAJIB melalui verifikasi/koreksi manual oleh Admin Gudang (BR-12, BR-13) sebelum masuk ke database transaksi resmi.

3. Alur Utama Sistem (Scope MVP):
   - Auth & Role-based Access (Admin Gudang, Karyawan, Manajer/Pimpinan).
   - Master Data Barang & Inventori.
   - Transaksi Barang Masuk/Keluar & Peminjaman/Pengembalian.
   - Modul AI Parsing Dokumen (Nota/Bukti) -> Verifikasi Admin -> Simpan Transaksi.
   - Modul AI Demand Forecasting -> Hitung Auto-Reorder Point -> Tampilkan Peringatan Stok Kritis pada Dashboard & Laporan.
--------------------------------------------------------------------------------

[Format Output HLD]

### 1) Diagram Arsitektur Sistem (Gunakan Format Mermaid)
Sajikan diagram aliran/blok komponen dari:
`Client (Web Browser)` → `Web Server / Backend API (PHP)` → `AI Service (Python / Cloud Service)` → `Data Store (MySQL & Storage File)` → `Fallback Mechanism`.

### 2) Deskripsi Komponen & Decision Trade-Off
- Jelaskan peran, tanggung jawab utama, dan rekomendasi teknologi spesifik untuk tiap komponen.
- **Tabel Trade-off Keputusan AI** (Sajikan perbandingan strategis: On-Device/Self-Hosted vs Cloud API Service untuk OCR dan Forecasting) berdasarkan parameter:
  * Akurasi, Latensi, Biaya, Privasi, Effort Pengembangan, dan berikan **Rekomendasi Arsitektur Final**.
- Berikan alasan (1–2 kalimat) untuk setiap keputusan teknis utama beserta alternatifnya.

### 3) Aliran Data End-to-End Fitur AI (End-to-End Data Flow)
Petakan alur pemrosesan data secara sistematis untuk kedua fitur AI:
`Input Data/File` → `Preprocessing` → `Inference (Model Execution)` → `Postprocessing / Parsing` → `Admin Human-in-the-Loop Validation` → `Penyimpanan DB`.
- **Wajib Sertakan**: Titik Penanganan Gagal/Fallback Mechanism (misal: jika OCR gagal/skor confidence rendah atau data historis forecasting tidak mencukupi/kosong).

### 4) Kontrak Antarkomponen Tingkat Tinggi (High-Level API Contract)
Rincikan antarmuka/skema komunikasi utama antarkomponen:
- **REST API Endpoint Utama** (Auth, Transaksi, Trigger OCR, Trigger Forecasting).
- **Format Data Payload** (JSON Request & Response).
- **Pemicu/Event** (Synchronous HTTP vs Asynchronous Batch Job).

### 5) Penempatan Security & Privacy by Design
- **Autentikasi & Otorisasi**: Skema manajemen sesi/token & RBAC.
- **Enkripsi**: Data in-transit (HTTPS/TLS) & Data at-rest (Password hashing BCRYPT, storage dokumen).
- **Privasi Data**: Penanganan file upload nota/bukti transaksi (retensi & pembersihan file).
- **Logging & Audit Trail**: Pencatatan aktivitas transaksi dan perubahan stok oleh pengguna.

### 6) Lingkungan Deployment Ringkas (Environment Topology)
Gambarkan topologi staging & deployment sederhana yang hemat biaya untuk skala prototype MVP:
- **Development Environment** (Local setup).
- **Production / Staging Environment** (Hosting VPS Murah / Cloud Free-tier, Web Server Nginx/Apache, MySQL, Python Service).

[Aturan Ketat]
- Hanya desain arsitektur berdasarkan FR/NFR dan User Stories yang ada; DILARANG menambah fitur bisnis baru. Jika terdapat gap teknis, tandai dengan `[ASUMSI-XX]`.
- JANGAN Masuk ke detail kodingan, class diagram internal, method signature, atau skema query SQL detail (karena itu ranah Low-Level Design / LLD).
- Gunakan Bahasa Indonesia baku, profesional, serta format Markdown rapi dan terstruktur.


[Peran] 
Kamu adalah Software Engineer Senior yang ahli dalam menerjemahkan High-Level Design (HLD) menjadi dokumen Low-Level Design (LLD) teknis yang terstruktur, konkret, dan siap diimplementasikan oleh tim pengembang.

[Tugas] 
Buat DRAF Low-Level Design (LLD) ringkas untuk fitur-fitur berprioritas **Must Have** (termasuk fitur AI inti) dari "Smart Inventory & Stock Demand Forecasting System" berdasarkan SRS dan HLD yang dilampirkan.

[Konteks & Acuan Landasan]
--------------------------------------------------------------------------------
1. Stack & Pola Arsitektur:
   - Backend Utama: PHP Framework (Laravel / CodeIgniter 4) — REST API Architecture.
   - AI Micro-Service: Python (FastAPI) — Tesseract OCR & Scikit-Learn/Statsmodels Demand Forecasting.
   - Database: MySQL.
   - Design Pattern Backend: Service-Repository Pattern / Clean Architecture Sederhana (Controller -> Service -> Repository -> Model).

2. Fitur Inti (Must Have) yang Harus Didesain di LLD:
   - **Fitur 1**: Transaksi Stok & Peminjaman (Barang Masuk/Keluar, Peminjaman/Pengembalian, Transaksi Stok).
   - **Fitur 2 (AI ★)**: OCR & Intelligent Document Parsing (Upload Nota/Bukti → Processing AI → Parsing → Admin Verification → Storage).
   - **Fitur 3 (AI ★)**: Demand Forecasting & Auto-Reorder Point (Pengolahan Data Historis → Model Inference → Hitung Reorder Point → Indikator Stok Kritis).

3. Konstrain & Aturan Kualitas (NFR & BR):
   - NFR-01 s.d. NFR-03: Akurasi OCR ≥80%, Akurasi Forecasting ≥80%, Akurasi Pencatatan Stok ≥90%.
   - NFR-07: Latensi Pemrosesan AI ≤10 detik/transaksi.
   - BR-10 & BR-11: Reorder Point & Forecasting HANYA sebagai *decision support* (bukan pemesanan otomatis).
   - BR-12 & BR-13: Hasil OCR WAJIB diverifikasi/dikoreksi Admin Gudang sebelum disimpan sebagai transaksi resmi.
--------------------------------------------------------------------------------

[Format Output LLD]

### 1) Desain Modul & Class (Service-Repository Pattern)
Rancang modul/class utama dalam bahasa Inggris untuk 3 fitur Must Have di atas (Termasuk Controller, Service, dan Repository). Rincikan:
- **Nama Class & Layer Responsibility**: (mis. `DocumentParsingService`, `InventoryRepository`).
- **Key Attributes**: Nama properti dan tipe datanya.
- **Main Methods**: Nama method, parameter input, tipe *return value*, dan deskripsi logika singkatnya.

### 2) Skema Data & Database Schema (MySQL / ERD Teks)
Buat rancangan tabel database terelasi (DDL SQL atau ERD Teks) yang mencakup entitas utama:
- `users`, `roles`
- `items` (master data barang)
- `stock_transactions` (barang masuk/keluar)
- `item_borrowings` (peminjaman & pengembalian barang)
- `documents` (file upload & teks/hasil ekstraksi OCR)
- `demand_forecasts` (hasil prediksi & reorder point)
*Sertakan Primary Key, Foreign Key, Data Types, Constraints (NOT NULL, UNIQUE, DEFAULT), dan Indexes.*

### 3) Spesifikasi API Detail (Endpoint Inti)
Rincikan kontrak API teknis untuk endpoint kritis berikut:
1. `POST /api/v1/documents/ocr-parse` (Upload & Trigger OCR)
2. `POST /api/v1/transactions` (Simpan Transaksi setelah Verifikasi OCR)
3. `POST /api/v1/ai/forecast` (Trigger/Retrieve Demand Forecasting & Reorder Point)
Sajikan untuk setiap endpoint:
- **Method & Endpoint Path**
- **Request Headers & Payload** (JSON / Multipart form-data)
- **Response Payload Sukses (200/201 OK)** dengan contoh JSON konkret.
- **Daftar Error Codes** (400 Bad Request, 422 Unprocessable, 500/504 Timeout AI).

### 4) Alur & Sequence Detail Fitur AI (dengan Timeout & Fallback)
Gambarkan urutan alur teknis (textual sequence) untuk:
- Alur **AI OCR Document Parsing**:
  `Client Upload` → `Backend Store File` → `HTTP Call FastAPI AI` → `Execution (Time-limit 10s)` → `Success/Timeout/Failure Handling` → `Fallback Status ('needs_manual_input')` → `Admin UI Correction`.
- Alur **AI Demand Forecasting**:
  `Trigger/Job` → `Fetch Historical Data` → `FastAPI ML Model` → `Validation Data Threshold` → `Fallback jika Data Historis < Minimum Threshold` → `Save to Forecast DB`.

### 5) Rancangan Error Handling, Retry, & Fallback Strategy
Rincikan penanganan kegagalan sistem & AI:
- **Circuit Breaker / Timeout**: Batas waktu eksekusi request ke Service Python (max 10 detik).
- **Retry Mechanism**: Aturan *exponential backoff* untuk transient error.
- **Pesan Error Ramah Pengguna**: Format respons *user-friendly* tanpa mengekspos *stack trace* internal.
- **Fallback Ke Modul Manual**: Langkah konkret jika service AI mati (*down*) agar operasional gudang tidak terhenti.

### 6) Opsi Pilihan Library/Teknologi (Decision Options)
Jika ada komponen detail yang belum diputuskan (misal: Library OCR Python, Library Job Queue, JWT vs Session Package), sajikan:
- Sarankan **2 Opsi** per komponen.
- Kriteria pembeda (Kemudahan, Performa, Effort).
- Tuliskan format placeholder: `[KEPUTUSAN TIM: ...]` yang wajib diisi oleh tim teknis.

### 7) Matriks Traceability (Keterlacakan)
Tabel pemetaan: **Elemen Desain LLD (Class/Table/API)** ↔ **ID FR / NFR / BR** terkait.

[Aturan Ketat Penulisan]
- **Strictly No Requirement Alteration**: Turunkan desain MURNI dari SRS dan HLD. DILARANG menambah fitur bisnis baru.
- **Bahasa**: Nama Class, Interface, Method, Database Column, dan Field JSON WAJIB menggunakan **Bahasa Inggris** (Standard Naming Conventions). Penjelasan konteks dan deskripsi menggunakan **Bahasa Indonesia Baku**.
- Gunakan format Markdown yang rapi, bersih, dan terstruktur.