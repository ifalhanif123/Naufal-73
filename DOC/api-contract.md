# API Contract
## Smart Inventory & Stock Demand Forecasting System

### 1. Tujuan

API dirancang sebagai kontrak REST API untuk aplikasi pengelolaan stok PT Jambi Agung Lestari. Kontrak mencakup autentikasi, master barang, transaksi stok, peminjaman, OCR dokumen, verifikasi dokumen, forecasting kebutuhan stok, dan laporan stok.

### 2. Stack

- Backend: FastAPI / Python
- Data validation: Pydantic v2
- Database: PostgreSQL/SQLite sesuai keputusan proyek PTM-05
- Format komunikasi: JSON
- Upload OCR: multipart/form-data
- Authentication: Bearer JWT

### 3. Endpoint

| Method | Endpoint | Fungsi | Tag |
|---|---|---|---|
| POST | `/api/v1/auth/login` | Login pengguna | Auth |
| POST | `/api/v1/documents/ocr-parse` | OCR dokumen | Documents, AI |
| GET | `/api/v1/documents/{id}` | Detail/status dokumen | Documents |
| POST | `/api/v1/documents/{id}/verify` | Verifikasi OCR | Documents, AI |
| POST | `/api/v1/transactions` | Transaksi stok | Transactions |
| GET | `/api/v1/transactions` | Riwayat transaksi | Transactions |
| GET | `/api/v1/transactions/{id}` | Detail transaksi | Transactions |
| POST | `/api/v1/borrowings` | Peminjaman | Borrowings |
| PUT | `/api/v1/borrowings/{id}/return` | Pengembalian | Borrowings |
| GET | `/api/v1/borrowings` | Daftar/status peminjaman | Borrowings |
| POST | `/api/v1/ai/forecast` | Forecasting kebutuhan stok | Forecasts, AI |
| GET | `/api/v1/items` | Master barang/stok | Items |
| GET | `/api/v1/reports/stock` | Laporan stok | Items |

Tidak ditambahkan endpoint di luar daftar LLD.

### 4. Keputusan desain

1. JWT digunakan sebagai Bearer Authentication.
2. Password tidak pernah dikembalikan pada response.
3. `user_id` transaksi berasal dari pengguna terautentikasi, bukan field yang bebas dikirim client.
4. `verified` transaksi ditentukan backend.
5. Dokumen OCR awalnya dapat berada pada status `needs_verification`.
6. Hasil OCR wajib diverifikasi Admin sebelum digunakan sebagai transaksi stok resmi.
7. Forecasting dan reorder point hanya menjadi decision support; tidak ada pembelian otomatis.
8. Endpoint AI menyediakan respons `422` untuk data tidak mencukupi/confidence rendah dan `504` untuk timeout.
9. Nilai confidence dibatasi 0 sampai 1.
10. Forecast period yang tersedia pada ERD adalah `monthly`.

### 5. Keamanan

- Semua endpoint selain login menggunakan Bearer JWT.
- `password_hash` tidak pernah dimasukkan ke response API.
- Endpoint verifikasi dokumen membutuhkan otorisasi Admin.
- File OCR divalidasi berdasarkan format upload dan tipe dokumen.
- Data internal seperti kredensial tidak diekspos.

### 6. Aturan error

- `400`: request/data bisnis tidak valid.
- `401`: token tidak ada atau tidak valid.
- `403`: pengguna tidak memiliki hak akses.
- `404`: resource tidak ditemukan.
- `422`: validasi gagal, confidence rendah, atau data forecasting tidak mencukupi.
- `500`: kesalahan internal server.
- `504`: proses AI melebihi batas waktu.

### 7. Sinkronisasi dengan ERD

Schema API menggunakan entitas:
`roles`, `users`, `items`, `stock_transactions`, `item_borrowings`, `documents`, dan `demand_forecasts`.

Field utama API diselaraskan dengan field ERD, termasuk enum status, foreign key, nullable field, dan tipe waktu.

### 8. Gap/Asumsi

Tidak ada `[ASUMSI-XX]` baru yang diperlukan pada versi final ini untuk field utama karena struktur ERD yang diberikan telah menjadi acuan penyelarasan OpenAPI.
