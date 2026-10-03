# ERD - Smart Inventory & Stock Demand Forecasting System

```mermaid
erDiagram
    roles ||--o{ users : "possesses"
    users ||--o{ stock_transactions : "creates"
    users ||--o{ item_borrowings : "borrows"
    users ||--o{ documents : "uploads"
    users ||--o{ documents : "verifies"
    items ||--o{ stock_transactions : "referenced_in"
    items ||--o{ item_borrowings : "borrowed_in"
    items ||--o{ demand_forecasts : "analyzed_in"
    documents o|--o| stock_transactions : "supports"

    roles {
        bigint id PK
        string name UK "admin_gudang, karyawan, manajer"
        datetime created_at
        datetime updated_at
    }

    users {
        bigint id PK
        bigint role_id FK
        string username UK
        string password_hash
        datetime created_at
        datetime updated_at
    }

    items {
        bigint id PK
        string code UK
        string name
        string description NULL
        string unit
        double stock
        double minimum_stock
        datetime created_at
        datetime updated_at
    }

    stock_transactions {
        bigint id PK
        bigint item_id FK
        bigint user_id FK
        bigint document_id FK NULL
        string transaction_type "in, out"
        double quantity
        datetime transaction_date
        string notes NULL
        boolean verified
        datetime created_at
        datetime updated_at
    }

    item_borrowings {
        bigint id PK
        bigint item_id FK
        bigint borrower_id FK
        double quantity
        string status "borrowed, returned"
        datetime borrowing_date
        datetime expected_return_date NULL
        datetime returned_at NULL
        string notes NULL
        datetime created_at
        datetime updated_at
    }

    documents {
        bigint id PK
        bigint user_id FK
        string file_name
        string file_path
        string mime_type
        string document_type "receipt, borrowing_evidence"
        string status "uploaded, processing, needs_verification, verified, rejected, needs_manual_input, failed"
        text ocr_text NULL
        json extracted_data NULL
        float confidence NULL
        bigint verified_by FK NULL
        datetime verified_at NULL
        datetime created_at
        datetime updated_at
    }

    demand_forecasts {
        bigint id PK
        bigint item_id FK
        string forecast_period "monthly"
        double forecast_value
        double reorder_point
        double current_stock
        string stock_status "normal, critical, out_of_stock"
        string model_name NULL
        float model_accuracy NULL
        datetime processed_at
        datetime created_at
        datetime updated_at
    }
```

## Constraint utama

- `roles.name` unique.
- `users.username` unique.
- `items.code` unique.
- `stock_transactions.transaction_type`: `in` atau `out`.
- `item_borrowings.status`: `borrowed` atau `returned`.
- `documents.document_type`: `receipt` atau `borrowing_evidence`.
- `documents.status`: `uploaded`, `processing`, `needs_verification`, `verified`, `rejected`, `needs_manual_input`, `failed`.
- `documents.confidence`: 0 sampai 1 apabila tersedia.
- `demand_forecasts.forecast_period`: `monthly`.
- `demand_forecasts.stock_status`: `normal`, `critical`, `out_of_stock`.
- Foreign key digunakan pada seluruh relasi yang ditunjukkan pada ERD.
- `stock_transactions.document_id`, `documents.verified_by`, dan beberapa field tanggal pengembalian bersifat nullable sesuai ERD.
