Berikut DRAF **LLD ringkas dan siap diturunkan ke implementasi**, dengan nama class, method, column, dan JSON field menggunakan bahasa Inggris. Saya menjaga desain tetap mengikuti HLD/SRS dan menandai keputusan yang belum ditentukan sebagai `[KEPUTUSAN TIM: ...]`.

# LOW-LEVEL DESIGN (LLD)

## Smart Inventory & Stock Demand Forecasting System

---

# 1. Desain Modul & Class

Arsitektur backend menggunakan pola:

```text
Controller
    ↓
Service
    ↓
Repository
    ↓
Model
    ↓
MySQL
```

Untuk fitur AI:

```text
PHP Controller
    ↓
AI Service
    ↓
Python FastAPI
    ↓
OCR / Forecasting Engine
```

## 1.1 Feature 1 — Stock Transaction & Borrowing

### A. Controller Layer

| Class                   | Responsibility                                                                 |
| ----------------------- | ------------------------------------------------------------------------------ |
| `TransactionController` | Menangani request barang masuk/keluar dan menyimpan transaksi setelah validasi |
| `BorrowingController`   | Menangani proses peminjaman dan pengembalian barang                            |

### `TransactionController`

**Key Attributes**

```text
transactionService: TransactionService
```

**Main Methods**

| Method      | Parameter                           | Return         | Deskripsi                              |
| ----------- | ----------------------------------- | -------------- | -------------------------------------- |
| `create()`  | `CreateTransactionRequest $request` | `JsonResponse` | Memvalidasi dan membuat transaksi stok |
| `show()`    | `int $transactionId`                | `JsonResponse` | Mengambil detail transaksi             |
| `history()` | `TransactionFilter $filter`         | `JsonResponse` | Mengambil riwayat transaksi            |

### `BorrowingController`

**Key Attributes**

```text
borrowingService: BorrowingService
```

**Main Methods**

| Method         | Parameter                         | Return         | Deskripsi                     |
| -------------- | --------------------------------- | -------------- | ----------------------------- |
| `create()`     | `CreateBorrowingRequest $request` | `JsonResponse` | Membuat data peminjaman       |
| `returnItem()` | `int $borrowingId`                | `JsonResponse` | Memproses pengembalian barang |
| `show()`       | `int $borrowingId`                | `JsonResponse` | Mengambil detail peminjaman   |
| `status()`     | `BorrowingFilter $filter`         | `JsonResponse` | Mengambil status peminjaman   |

---

## 1.2 Service Layer

### `TransactionService`

**Key Attributes**

```text
transactionRepository: TransactionRepository
itemRepository: ItemRepository
```

**Main Methods**

| Method                        | Parameter                                | Return             | Deskripsi                                    |
| ----------------------------- | ---------------------------------------- | ------------------ | -------------------------------------------- |
| `createTransaction()`         | `TransactionData $data`                  | `StockTransaction` | Memvalidasi transaksi dan memperbarui stok   |
| `validateStockAvailability()` | `int $itemId, int $quantity`             | `bool`             | Memastikan stok cukup untuk transaksi keluar |
| `calculateStockChange()`      | `string $transactionType, int $quantity` | `int`              | Menentukan perubahan stok                    |
| `getTransactionHistory()`     | `TransactionFilter $filter`              | `Collection`       | Mengambil riwayat transaksi                  |

Aturan:

```text
barang_masuk  → stock bertambah
barang_keluar → stock berkurang
```

Transaksi yang menyebabkan stok tidak sesuai harus ditolak.

---

### `BorrowingService`

**Key Attributes**

```text
borrowingRepository: BorrowingRepository
itemRepository: ItemRepository
```

**Main Methods**

| Method                 | Parameter                 | Return          | Deskripsi                        |
| ---------------------- | ------------------------- | --------------- | -------------------------------- |
| `createBorrowing()`    | `BorrowingData $data`     | `ItemBorrowing` | Membuat transaksi peminjaman     |
| `processReturn()`      | `int $borrowingId`        | `ItemBorrowing` | Mengubah status menjadi returned |
| `getBorrowingStatus()` | `BorrowingFilter $filter` | `Collection`    | Mengambil status peminjaman      |

---

## 1.3 Repository Layer

### `TransactionRepository`

**Key Attributes**

```text
model: StockTransaction
```

**Main Methods**

| Method       | Parameter                       | Return              |
| ------------ | ------------------------------- | ------------------- |
| `create()`   | `TransactionData $data`         | `StockTransaction`  |
| `findById()` | `int $transactionId`            | `?StockTransaction` |
| `findAll()`  | `TransactionFilter $filter`     | `Collection`        |
| `save()`     | `StockTransaction $transaction` | `StockTransaction`  |

---

### `BorrowingRepository`

| Method           | Parameter                          | Return           |
| ---------------- | ---------------------------------- | ---------------- |
| `create()`       | `BorrowingData $data`              | `ItemBorrowing`  |
| `findById()`     | `int $borrowingId`                 | `?ItemBorrowing` |
| `updateStatus()` | `int $borrowingId, string $status` | `ItemBorrowing`  |
| `findAll()`      | `BorrowingFilter $filter`          | `Collection`     |

---

### `ItemRepository`

| Method              | Parameter                    | Return       |
| ------------------- | ---------------------------- | ------------ |
| `findById()`        | `int $itemId`                | `?Item`      |
| `updateStock()`     | `int $itemId, int $quantity` | `Item`       |
| `getCurrentStock()` | `int $itemId`                | `int`        |
| `findAll()`         | `ItemFilter $filter`         | `Collection` |

---

# 2. Feature 2 — AI OCR & Intelligent Document Parsing

Alur internal:

```text
DocumentController
        ↓
DocumentParsingService
        ↓
DocumentRepository
        ↓
PythonAIClient
        ↓
FastAPI OCR Service
        ↓
Tesseract
        ↓
Parsing Result
        ↓
Admin Verification
```

## 2.1 Controller

### `DocumentController`

**Key Attributes**

```text
documentParsingService: DocumentParsingService
```

**Main Methods**

| Method             | Parameter                                 | Return         | Deskripsi                             |
| ------------------ | ----------------------------------------- | -------------- | ------------------------------------- |
| `uploadAndParse()` | `UploadedFile $file`                      | `JsonResponse` | Menyimpan dokumen dan menjalankan OCR |
| `showResult()`     | `int $documentId`                         | `JsonResponse` | Mengambil hasil OCR/parsing           |
| `verifyResult()`   | `int $documentId, VerificationData $data` | `JsonResponse` | Memvalidasi atau mengoreksi hasil AI  |

---

## 2.2 `DocumentParsingService`

**Key Attributes**

```text
documentRepository: DocumentRepository
fileStorage: FileStorage
aiClient: PythonAIClient
```

**Main Methods**

| Method               | Parameter                                 | Return                | Deskripsi                                      |
| -------------------- | ----------------------------------------- | --------------------- | ---------------------------------------------- |
| `uploadAndParse()`   | `UploadedFile $file, int $userId`         | `DocumentParseResult` | Menyimpan file dan memanggil AI                |
| `validateDocument()` | `UploadedFile $file`                      | `bool`                | Memvalidasi file sebelum OCR                   |
| `verifyResult()`     | `int $documentId, VerificationData $data` | `Document`            | Menyimpan hasil yang telah diverifikasi        |
| `markManualInput()`  | `int $documentId`                         | `Document`            | Mengubah status menjadi kebutuhan input manual |

Hasil AI **tidak boleh langsung menjadi transaksi resmi**.

---

## 2.3 `PythonAIClient`

Class ini merupakan client pada backend PHP yang berkomunikasi dengan FastAPI.

**Key Attributes**

```text
baseUrl: string
timeoutSeconds: int
```

**Main Methods**

| Method            | Parameter          | Return      | Deskripsi                         |
| ----------------- | ------------------ | ----------- | --------------------------------- |
| `parseDocument()` | `string $filePath` | `OCRResult` | Mengirim dokumen ke AI Service    |
| `checkHealth()`   | none               | `bool`      | Memeriksa ketersediaan AI Service |

Konfigurasi:

```text
timeoutSeconds = 10
```

Nilai tersebut mengikuti NFR-07.

---

## 2.4 `OCRResult`

**Key Attributes**

```text
status: string
confidence: float
documentNumber: ?string
itemName: ?string
quantity: ?int
rawText: ?string
```

Contoh status:

```text
completed
needs_verification
needs_manual_input
failed
```

---

## 2.5 `DocumentRepository`

| Method               | Parameter                                 | Return      |
| -------------------- | ----------------------------------------- | ----------- |
| `create()`           | `DocumentData $data`                      | `Document`  |
| `findById()`         | `int $documentId`                         | `?Document` |
| `saveOCRResult()`    | `int $documentId, OCRResult $result`      | `Document`  |
| `saveVerification()` | `int $documentId, VerificationData $data` | `Document`  |
| `updateStatus()`     | `int $documentId, string $status`         | `Document`  |

---

# 3. Feature 3 — Demand Forecasting & Reorder Point

Alur:

```text
ForecastController
       ↓
ForecastService
       ↓
TransactionRepository
       ↓
PythonAIClient
       ↓
FastAPI Forecasting
       ↓
Scikit-Learn / Statsmodels
       ↓
Forecast Result
       ↓
Reorder Point
       ↓
Stock Critical Indicator
```

## 3.1 `ForecastController`

**Key Attributes**

```text
forecastService: ForecastService
```

**Main Methods**

| Method       | Parameter                  | Return         | Deskripsi                     |
| ------------ | -------------------------- | -------------- | ----------------------------- |
| `forecast()` | `ForecastRequest $request` | `JsonResponse` | Memulai/mengambil forecasting |
| `show()`     | `int $forecastId`          | `JsonResponse` | Mengambil hasil forecasting   |

---

## 3.2 `ForecastService`

**Key Attributes**

```text
forecastRepository: ForecastRepository
transactionRepository: TransactionRepository
itemRepository: ItemRepository
aiClient: PythonAIClient
```

**Main Methods**

| Method                     | Parameter                                | Return           | Deskripsi                                        |
| -------------------------- | ---------------------------------------- | ---------------- | ------------------------------------------------ |
| `generateForecast()`       | `ForecastRequest $request`               | `DemandForecast` | Mengambil data historis dan meminta prediksi     |
| `validateHistoricalData()` | `int $itemId`                            | `bool`           | Memastikan data memenuhi minimum yang dibutuhkan |
| `calculateReorderPoint()`  | `ForecastResult $result`                 | `float`          | Menghasilkan indikator reorder point             |
| `determineStockStatus()`   | `int $currentStock, float $reorderPoint` | `string`         | Menentukan indikator kondisi stok                |
| `saveForecast()`           | `ForecastResult $result`                 | `DemandForecast` | Menyimpan hasil forecasting                      |

Minimum jumlah data historis **belum ditentukan dalam SRS/HLD**, sehingga:

```text
[KEPUTUSAN TIM: Tentukan minimum historical data untuk forecasting]
```

---

## 3.3 `ForecastRepository`

| Method               | Parameter                  | Return            |
| -------------------- | -------------------------- | ----------------- |
| `create()`           | `ForecastData $data`       | `DemandForecast`  |
| `findById()`         | `int $forecastId`          | `?DemandForecast` |
| `findLatestByItem()` | `int $itemId`              | `?DemandForecast` |
| `save()`             | `DemandForecast $forecast` | `DemandForecast`  |

---

## 3.4 `ForecastResult`

**Key Attributes**

```text
itemId: int
forecastValue: float
reorderPoint: float
stockStatus: string
modelAccuracy: ?float
processedAt: DateTime
```

`modelAccuracy` bersifat nullable karena nilai evaluasi model tidak selalu dihasilkan pada setiap inference.

Target kualitas:

```text
Forecasting accuracy >= 80%
```

---

# 4. Database Schema

## 4.1 Entity Relationship Diagram — Text

```text
roles
  │
  │ 1:N
  ▼
users
  │
  ├───────────────┐
  │               │
  │ 1:N           │ 1:N
  ▼               ▼
documents      stock_transactions
  │                 │
  │ 1:N             │ N:1
  │                 ▼
  │               items
  │                 ▲
  │                 │
  │                 │ N:1
  ▼                 │
demand_forecasts ───┘

users
  │
  │ 1:N
  ▼
item_borrowings
  │
  │ N:1
  ▼
items
```

---

## 4.2 `roles`

| Column       | Type            | Constraint         |
| ------------ | --------------- | ------------------ |
| `id`         | BIGINT UNSIGNED | PK, AUTO_INCREMENT |
| `name`       | VARCHAR(50)     | NOT NULL, UNIQUE   |
| `created_at` | TIMESTAMP       | NULL               |
| `updated_at` | TIMESTAMP       | NULL               |

Index:

```text
UNIQUE INDEX idx_roles_name (name)
```

---

## 4.3 `users`

| Column       | Type            | Constraint         |
| ------------ | --------------- | ------------------ |
| `id`         | BIGINT UNSIGNED | PK, AUTO_INCREMENT |
| `role_id`    | BIGINT UNSIGNED | NOT NULL, FK       |
| `name`       | VARCHAR(100)    | NOT NULL           |
| `username`   | VARCHAR(100)    | NOT NULL, UNIQUE   |
| `password`   | VARCHAR(255)    | NOT NULL           |
| `created_at` | TIMESTAMP       | NULL               |
| `updated_at` | TIMESTAMP       | NULL               |

Foreign key:

```text
role_id → roles.id
```

Index:

```text
UNIQUE INDEX idx_users_username (username)
INDEX idx_users_role_id (role_id)
```

---

## 4.4 `items`

| Column       | Type            | Constraint          |
| ------------ | --------------- | ------------------- |
| `id`         | BIGINT UNSIGNED | PK, AUTO_INCREMENT  |
| `item_code`  | VARCHAR(50)     | NOT NULL, UNIQUE    |
| `name`       | VARCHAR(150)    | NOT NULL            |
| `unit`       | VARCHAR(30)     | NOT NULL            |
| `stock`      | INT UNSIGNED    | NOT NULL, DEFAULT 0 |
| `created_at` | TIMESTAMP       | NULL                |
| `updated_at` | TIMESTAMP       | NULL                |

Index:

```text
UNIQUE INDEX idx_items_code (item_code)
INDEX idx_items_name (name)
```

---

## 4.5 `stock_transactions`

| Column             | Type            | Constraint         |
| ------------------ | --------------- | ------------------ |
| `id`               | BIGINT UNSIGNED | PK, AUTO_INCREMENT |
| `item_id`          | BIGINT UNSIGNED | NOT NULL, FK       |
| `user_id`          | BIGINT UNSIGNED | NOT NULL, FK       |
| `document_id`      | BIGINT UNSIGNED | NULL, FK           |
| `transaction_type` | ENUM            | NOT NULL           |
| `quantity`         | INT UNSIGNED    | NOT NULL           |
| `transaction_date` | DATETIME        | NOT NULL           |
| `notes`            | TEXT            | NULL               |
| `created_at`       | TIMESTAMP       | NULL               |
| `updated_at`       | TIMESTAMP       | NULL               |

`transaction_type`:

```text
in
out
```

Foreign keys:

```text
item_id     → items.id
user_id     → users.id
document_id → documents.id
```

Indexes:

```text
INDEX idx_transactions_item_id (item_id)
INDEX idx_transactions_user_id (user_id)
INDEX idx_transactions_date (transaction_date)
INDEX idx_transactions_type (transaction_type)
```

---

## 4.6 `item_borrowings`

| Column        | Type            | Constraint                   |
| ------------- | --------------- | ---------------------------- |
| `id`          | BIGINT UNSIGNED | PK, AUTO_INCREMENT           |
| `item_id`     | BIGINT UNSIGNED | NOT NULL, FK                 |
| `user_id`     | BIGINT UNSIGNED | NOT NULL, FK                 |
| `quantity`    | INT UNSIGNED    | NOT NULL                     |
| `borrowed_at` | DATETIME        | NOT NULL                     |
| `returned_at` | DATETIME        | NULL                         |
| `status`      | ENUM            | NOT NULL, DEFAULT `borrowed` |
| `notes`       | TEXT            | NULL                         |
| `created_at`  | TIMESTAMP       | NULL                         |
| `updated_at`  | TIMESTAMP       | NULL                         |

`status`:

```text
borrowed
returned
```

Foreign keys:

```text
item_id → items.id
user_id → users.id
```

Indexes:

```text
INDEX idx_borrowings_item_id (item_id)
INDEX idx_borrowings_user_id (user_id)
INDEX idx_borrowings_status (status)
INDEX idx_borrowings_borrowed_at (borrowed_at)
```

---

## 4.7 `documents`

| Column           | Type            | Constraint                   |
| ---------------- | --------------- | ---------------------------- |
| `id`             | BIGINT UNSIGNED | PK, AUTO_INCREMENT           |
| `user_id`        | BIGINT UNSIGNED | NOT NULL, FK                 |
| `file_name`      | VARCHAR(255)    | NOT NULL                     |
| `file_path`      | VARCHAR(500)    | NOT NULL                     |
| `mime_type`      | VARCHAR(100)    | NOT NULL                     |
| `raw_text`       | LONGTEXT        | NULL                         |
| `extracted_data` | JSON            | NULL                         |
| `confidence`     | DECIMAL(5,4)    | NULL                         |
| `status`         | ENUM            | NOT NULL, DEFAULT `uploaded` |
| `verified_at`    | DATETIME        | NULL                         |
| `verified_by`    | BIGINT UNSIGNED | NULL, FK                     |
| `created_at`     | TIMESTAMP       | NULL                         |
| `updated_at`     | TIMESTAMP       | NULL                         |

`status`:

```text
uploaded
processing
needs_verification
verified
needs_manual_input
failed
```

Foreign keys:

```text
user_id     → users.id
verified_by → users.id
```

Indexes:

```text
INDEX idx_documents_user_id (user_id)
INDEX idx_documents_status (status)
INDEX idx_documents_verified_by (verified_by)
```

---

## 4.8 `demand_forecasts`

| Column            | Type            | Constraint         |
| ----------------- | --------------- | ------------------ |
| `id`              | BIGINT UNSIGNED | PK, AUTO_INCREMENT |
| `item_id`         | BIGINT UNSIGNED | NOT NULL, FK       |
| `forecast_period` | VARCHAR(30)     | NOT NULL           |
| `forecast_value`  | DECIMAL(12,2)   | NOT NULL           |
| `reorder_point`   | DECIMAL(12,2)   | NOT NULL           |
| `stock_status`    | VARCHAR(30)     | NOT NULL           |
| `model_accuracy`  | DECIMAL(5,2)    | NULL               |
| `processed_at`    | DATETIME        | NOT NULL           |
| `created_at`      | TIMESTAMP       | NULL               |
| `updated_at`      | TIMESTAMP       | NULL               |

Foreign key:

```text
item_id → items.id
```

Indexes:

```text
INDEX idx_forecasts_item_id (item_id)
INDEX idx_forecasts_period (forecast_period)
INDEX idx_forecasts_status (stock_status)
INDEX idx_forecasts_processed_at (processed_at)
```

---

## 4.9 Catatan Integritas Data

1. `quantity` tidak boleh bernilai negatif.
2. `stock` tidak boleh bernilai negatif.
3. `verified_by` hanya diisi ketika hasil OCR telah diverifikasi.
4. `document_id` pada transaksi bersifat nullable karena transaksi dapat menggunakan input manual.
5. Hasil OCR dengan status `needs_verification` atau `needs_manual_input` tidak boleh menjadi transaksi resmi.
6. `reorder_point` hanya digunakan sebagai indikator/rekomendasi dan tidak memicu pembelian otomatis.

---

# 5. Spesifikasi API Detail

## 5.1 `POST /api/v1/documents/ocr-parse`

### Tujuan

Mengunggah nota/bukti dan menjalankan OCR serta intelligent document parsing.

### Headers

```http
Authorization: Bearer <token>
Content-Type: multipart/form-data
Accept: application/json
```

### Request

```text
multipart/form-data

file: <document>
```

Metadata tambahan tidak diwajibkan pada endpoint ini.

### Success — `200 OK`

```json
{
  "success": true,
  "message": "Document processed successfully",
  "data": {
    "document_id": 1001,
    "status": "needs_verification",
    "confidence": 0.86,
    "raw_text": "....",
    "extracted_data": {
      "document_number": "INV-001",
      "item_name": "Item A",
      "quantity": 20
    },
    "requires_verification": true
  }
}
```

### Error

| HTTP | Code                  | Kondisi                         |
| ---- | --------------------- | ------------------------------- |
| 400  | `INVALID_FILE`        | File tidak valid                |
| 401  | `UNAUTHENTICATED`     | User belum login                |
| 403  | `FORBIDDEN`           | User tidak memiliki hak         |
| 422  | `DOCUMENT_UNREADABLE` | Dokumen tidak dapat diproses    |
| 422  | `LOW_CONFIDENCE`      | Confidence di bawah target      |
| 504  | `AI_TIMEOUT`          | AI Service melewati batas waktu |
| 500  | `AI_SERVICE_ERROR`    | AI Service mengalami error      |

Response error:

```json
{
  "success": false,
  "error": {
    "code": "AI_TIMEOUT",
    "message": "Document processing could not be completed. Please enter the data manually."
  }
}
```

---

# 5.2 `POST /api/v1/transactions`

### Tujuan

Menyimpan transaksi setelah data, termasuk hasil OCR, diverifikasi oleh Admin.

### Headers

```http
Authorization: Bearer <token>
Content-Type: application/json
Accept: application/json
```

### Request

```json
{
  "item_id": 101,
  "transaction_type": "in",
  "quantity": 20,
  "document_id": 1001,
  "notes": "Verified document data"
}
```

### Success — `201 Created`

```json
{
  "success": true,
  "message": "Transaction created successfully",
  "data": {
    "transaction_id": 501,
    "item_id": 101,
    "transaction_type": "in",
    "quantity": 20,
    "stock": 120,
    "verified": true
  }
}
```

### Error

| HTTP | Code                    | Kondisi                                     |
| ---- | ----------------------- | ------------------------------------------- |
| 400  | `INVALID_TRANSACTION`   | Payload transaksi tidak valid               |
| 401  | `UNAUTHENTICATED`       | User belum login                            |
| 403  | `FORBIDDEN`             | Tidak memiliki hak transaksi                |
| 422  | `INSUFFICIENT_STOCK`    | Stok tidak mencukupi untuk transaksi keluar |
| 422  | `DOCUMENT_NOT_VERIFIED` | Dokumen OCR belum diverifikasi              |
| 422  | `INVALID_ITEM`          | Barang tidak ditemukan                      |
| 500  | `TRANSACTION_FAILED`    | Gagal menyimpan transaksi                   |

---

# 5.3 `POST /api/v1/ai/forecast`

### Tujuan

Menjalankan demand forecasting untuk barang tertentu dan menghasilkan indikator reorder point serta status stok.

### Headers

```http
Authorization: Bearer <token>
Content-Type: application/json
Accept: application/json
```

### Request

```json
{
  "item_id": 101,
  "forecast_period": "monthly"
}
```

### Success — `200 OK`

```json
{
  "success": true,
  "message": "Forecast generated successfully",
  "data": {
    "item_id": 101,
    "forecast_period": "monthly",
    "forecast_value": 35,
    "reorder_point": 40,
    "stock_status": "critical",
    "processed_at": "2026-09-21T13:00:00+07:00"
  }
}
```

### Error

| HTTP | Code                           | Kondisi                           |
| ---- | ------------------------------ | --------------------------------- |
| 400  | `INVALID_FORECAST_REQUEST`     | Request tidak valid               |
| 401  | `UNAUTHENTICATED`              | User belum login                  |
| 403  | `FORBIDDEN`                    | Tidak memiliki hak                |
| 422  | `INSUFFICIENT_HISTORICAL_DATA` | Data historis tidak mencukupi     |
| 422  | `INVALID_HISTORICAL_DATA`      | Data historis tidak valid         |
| 500  | `FORECAST_SERVICE_ERROR`       | Model gagal menghasilkan prediksi |
| 504  | `AI_TIMEOUT`                   | Forecasting melewati batas waktu  |

---

# 6. Sequence Detail Fitur AI

## 6.1 AI OCR Document Parsing

```text
Client
  │
  │ 1. Upload Document
  ▼
DocumentController
  │
  │ 2. Validate File
  ▼
DocumentParsingService
  │
  │ 3. Store File
  ▼
FileStorage
  │
  │ 4. Return File Reference
  ▼
DocumentParsingService
  │
  │ 5. HTTP POST
  ▼
FastAPI OCR Service
  │
  │ 6. OCR + Parsing
  │
  │ Maximum processing time: 10 seconds
  │
  ├── Success ────────────────┐
  │                            ▼
  │                     OCR Result
  │                            │
  │                            ▼
  │                     Backend Service
  │                            │
  │                            ▼
  │                     Admin Verification
  │
  ├── Low Confidence ─────────► needs_manual_input
  │
  ├── Processing Failure ─────► needs_manual_input
  │
  └── Timeout > 10 sec ───────► needs_manual_input
                                   │
                                   ▼
                            Admin Correction
                                   │
                                   ▼
                            Verified Document
                                   │
                                   ▼
                         Create Transaction
```

### Aturan

```text
confidence >= 0.80
    → tetap membutuhkan Admin Verification

confidence < 0.80
    → needs_manual_input / manual correction

timeout > 10 seconds
    → needs_manual_input

AI failure
    → needs_manual_input
```

---

## 6.2 AI Demand Forecasting

```text
ForecastController / Job
        │
        │ 1. Trigger Forecast
        ▼
ForecastService
        │
        │ 2. Fetch Historical Data
        ▼
TransactionRepository
        │
        │ 3. Historical Dataset
        ▼
ForecastService
        │
        │ 4. Validate Data Threshold
        │
        ├── Insufficient ──────► Fallback
        │                         │
        │                         ▼
        │                  No AI Prediction
        │
        └── Sufficient
                │
                ▼
        PythonAIClient
                │
                │ 5. HTTP Request
                ▼
        FastAPI Forecast Service
                │
                │ 6. Model Inference
                ▼
        Forecast Result
                │
                ▼
        ForecastService
                │
                │ 7. Reorder Point
                │
                ▼
        Stock Status
                │
                ▼
        ForecastRepository
                │
                ▼
        demand_forecasts
```

Minimum historical data:

```text
[KEPUTUSAN TIM: Tentukan minimum historical data]
```

---

# 7. Error Handling, Retry, dan Fallback

## 7.1 Timeout dan Circuit Breaker

Backend menggunakan timeout maksimum:

```text
AI request timeout = 10 seconds
```

Jika Python Service tidak memberikan response dalam batas tersebut:

```text
AI_TIMEOUT
     ↓
Stop current AI request
     ↓
Mark process as failed/manual
     ↓
Return user-friendly response
```

Circuit breaker dapat digunakan untuk mencegah backend terus-menerus memanggil AI Service yang sedang tidak tersedia.

Status:

```text
CLOSED
   ↓ repeated failures
OPEN
   ↓ cooldown
HALF_OPEN
   ↓ successful request
CLOSED
```

Durasi cooldown belum ditentukan:

```text
[KEPUTUSAN TIM: Tentukan circuit breaker cooldown]
```

---

## 7.2 Retry Mechanism

Retry hanya dilakukan untuk **transient error**, bukan untuk error validasi data.

Contoh:

```text
Attempt 1 → immediate
Attempt 2 → 500 ms
Attempt 3 → 1000 ms
```

Formula umum:

```text
delay = baseDelay × 2^(attempt - 1)
```

Maksimum retry:

```text
[KEPUTUSAN TIM: 2 atau 3 retry]
```

Retry **tidak dilakukan** untuk:

```text
400 Bad Request
401 Unauthorized
403 Forbidden
422 Validation Error
Low Confidence
Insufficient Historical Data
```

---

## 7.3 User-Friendly Error Response

Backend tidak boleh mengembalikan stack trace.

Contoh:

```json
{
  "success": false,
  "error": {
    "code": "AI_SERVICE_UNAVAILABLE",
    "message": "AI processing is temporarily unavailable. Please enter the data manually."
  }
}
```

Detail teknis hanya dicatat pada internal application log.

---

## 7.4 Fallback ketika AI Service Down

### OCR

```text
AI Service Down
      ↓
Backend detects connection failure
      ↓
Document status = needs_manual_input
      ↓
Admin enters/corrects transaction data
      ↓
Admin verifies
      ↓
Transaction saved
```

### Forecasting

```text
AI Service Down
      ↓
Forecasting unavailable
      ↓
No AI recommendation generated
      ↓
Current stock information remains available
```

Dengan demikian, kegagalan AI tidak menghentikan fungsi inventori dasar.

---

# 8. Opsi Library / Teknologi

## 8.1 OCR Library

| Opsi                    | Kelebihan                                | Kekurangan                                   | Effort          |
| ----------------------- | ---------------------------------------- | -------------------------------------------- | --------------- |
| **Tesseract**           | Open-source, self-hosted, biaya rendah   | Membutuhkan preprocessing agar hasil optimal | Rendah–Menengah |
| **Google Cloud Vision** | OCR dokumen relatif mudah diintegrasikan | Bergantung cloud dan biaya penggunaan        | Rendah          |

**Rekomendasi HLD:** Tesseract.

```text
[KEPUTUSAN TIM: Tesseract / Google Cloud Vision]
```

---

## 8.2 Python API Framework

| Opsi        | Kelebihan                                   | Kekurangan                                        | Effort |
| ----------- | ------------------------------------------- | ------------------------------------------------- | ------ |
| **FastAPI** | Ringan, API-oriented, validasi request baik | Perlu struktur service sendiri                    | Rendah |
| **Flask**   | Sederhana dan fleksibel                     | Beberapa komponen API perlu dikonfigurasi sendiri | Rendah |

```text
[KEPUTUSAN TIM: FastAPI / Flask]
```

---

## 8.3 Forecasting Library

| Opsi             | Kelebihan                                | Kekurangan                                | Cocok                   |
| ---------------- | ---------------------------------------- | ----------------------------------------- | ----------------------- |
| **Scikit-Learn** | Banyak algoritma ML dan mudah dievaluasi | Pemilihan fitur/model perlu eksperimen    | MVP                     |
| **Statsmodels**  | Kuat untuk model statistik/time series   | Lebih spesifik untuk pendekatan statistik | Forecasting time series |

```text
[KEPUTUSAN TIM: Scikit-Learn / Statsmodels]
```

Model final tidak ditetapkan pada LLD sebelum dilakukan pengujian dataset.

---

## 8.4 Authentication

| Opsi                       | Kelebihan                          | Kekurangan                                 |
| -------------------------- | ---------------------------------- | ------------------------------------------ |
| **Session Authentication** | Sederhana untuk web browser        | Kurang ideal untuk banyak client eksternal |
| **JWT**                    | Stateless dan cocok untuk REST API | Pengelolaan token lebih kompleks           |

Untuk aplikasi web MVP:

```text
[KEPUTUSAN TIM: Session / JWT]
```

---

## 8.5 Job Queue

| Opsi                                | Kelebihan                                 | Kekurangan                        |
| ----------------------------------- | ----------------------------------------- | --------------------------------- |
| **Laravel Queue / Framework Queue** | Integrasi dengan backend lebih mudah      | Bergantung implementasi framework |
| **Celery + Redis**                  | Cocok untuk pekerjaan Python asynchronous | Menambah komponen deployment      |

Rekomendasi awal untuk MVP adalah synchronous HTTP selama NFR-07 dapat dipenuhi.

```text
[KEPUTUSAN TIM: Synchronous / Queue]
```

---

## 8.6 File Storage

| Opsi                  | Kelebihan                                           | Kekurangan                 |
| --------------------- | --------------------------------------------------- | -------------------------- |
| **Local/VPS Storage** | Murah dan sederhana                                 | Bergantung storage server  |
| **Object Storage**    | Lebih scalable dan terpisah dari application server | Menambah biaya/konfigurasi |

```text
[KEPUTUSAN TIM: Local/VPS Storage / Object Storage]
```

---

# 9. Matriks Traceability

| Elemen LLD                | FR                  | NFR                    | BR                         |
| ------------------------- | ------------------- | ---------------------- | -------------------------- |
| `TransactionController`   | FR-04, FR-05        | NFR-03                 | BR-01, BR-02, BR-03        |
| `TransactionService`      | FR-04, FR-05, FR-09 | NFR-03                 | BR-02, BR-03               |
| `BorrowingController`     | FR-06, FR-07, FR-08 | NFR-14                 | BR-04, BR-05, BR-06, BR-07 |
| `BorrowingService`        | FR-06, FR-07        | NFR-14                 | BR-04, BR-05, BR-07        |
| `ItemRepository`          | FR-03, FR-04, FR-05 | NFR-03                 | BR-02, BR-03               |
| `documents`               | FR-14, FR-15, FR-16 | NFR-01, NFR-07         | BR-12, BR-13               |
| `DocumentController`      | FR-14, FR-15, FR-16 | NFR-01, NFR-07         | BR-12, BR-13               |
| `DocumentParsingService`  | FR-14, FR-15, FR-16 | NFR-01, NFR-03, NFR-07 | BR-12, BR-13               |
| `PythonAIClient`          | FR-14, FR-15, FR-11 | NFR-01, NFR-02, NFR-07 | BR-11, BR-12               |
| `ForecastController`      | FR-11, FR-12, FR-13 | NFR-02, NFR-07         | BR-09, BR-10, BR-11        |
| `ForecastService`         | FR-11, FR-12, FR-13 | NFR-02, NFR-07         | BR-09, BR-10, BR-11        |
| `demand_forecasts`        | FR-11, FR-12, FR-13 | NFR-02                 | BR-09, BR-10               |
| `items`                   | FR-03, FR-04, FR-05 | NFR-03                 | BR-02, BR-03               |
| `stock_transactions`      | FR-04, FR-05, FR-09 | NFR-03                 | BR-01, BR-02, BR-03, BR-08 |
| `item_borrowings`         | FR-06, FR-07, FR-08 | NFR-14                 | BR-04, BR-05, BR-06, BR-07 |
| `users` / `roles`         | FR-01, FR-02        | NFR-08, NFR-09         | —                          |
| Authentication Middleware | FR-01, FR-02        | NFR-08, NFR-09, NFR-10 | —                          |
| HTTPS/TLS                 | —                   | NFR-10, NFR-11         | —                          |
| Manual OCR Verification   | FR-16               | NFR-01, NFR-03         | BR-12, BR-13               |
| AI Timeout/Fallback       | FR-11, FR-14, FR-15 | NFR-07                 | BR-11, BR-12               |
| Forecasting Fallback      | FR-11, FR-12, FR-13 | NFR-02                 | BR-09, BR-11               |

---

# 10. Ringkasan Implementasi

Struktur implementasi tingkat tinggi yang dihasilkan dari LLD:

```text
PHP APPLICATION
│
├── Controllers
│   ├── TransactionController
│   ├── BorrowingController
│   ├── DocumentController
│   └── ForecastController
│
├── Services
│   ├── TransactionService
│   ├── BorrowingService
│   ├── DocumentParsingService
│   └── ForecastService
│
├── Repositories
│   ├── ItemRepository
│   ├── TransactionRepository
│   ├── BorrowingRepository
│   ├── DocumentRepository
│   └── ForecastRepository
│
├── AI Client
│   └── PythonAIClient
│
└── Models
    ├── User
    ├── Role
    ├── Item
    ├── StockTransaction
    ├── ItemBorrowing
    ├── Document
    └── DemandForecast


PYTHON FASTAPI SERVICE
│
├── OCR Module
│   ├── OCR Engine
│   └── Document Parser
│
└── Forecasting Module
    ├── Data Validation
    ├── Preprocessing
    ├── Model Inference
    └── Forecast Result
```

### Prinsip Implementasi yang Harus Dipertahankan

1. **Business logic tetap berada pada PHP Backend**, sedangkan Python bertanggung jawab terhadap proses AI.
2. **AI tidak boleh langsung menyimpan transaksi resmi.**
3. Hasil OCR harus melalui **Admin Verification** sebelum masuk ke `stock_transactions`.
4. Confidence OCR `< 80%` diarahkan ke proses verifikasi/manual.
5. Request AI memiliki batas waktu **maksimal 10 detik** sesuai NFR-07.
6. Forecasting yang gagal atau tidak memiliki data mencukupi tidak boleh menghasilkan rekomendasi seolah-olah valid.
7. `reorder_point` hanya menjadi **decision support**, bukan pemesanan otomatis.
8. Ketika AI tidak tersedia, transaksi inventori tetap dapat dilakukan melalui mekanisme manual.
9. Detail model forecasting final ditentukan berdasarkan eksperimen dataset, bukan diasumsikan pada level desain.
10. Nilai yang masih belum ditentukan ditandai dengan `[KEPUTUSAN TIM: ...]` sehingga dapat diputuskan sebelum implementasi.
