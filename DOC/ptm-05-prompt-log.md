# PTM-05 Prompt Log
## Smart Inventory & Stock Demand Forecasting System

| No | Target Prompt | Alat AI & Versi | Ringkasan Prompt | Kualitas Output (1-5) | Revisi Manual |
|---|---|---|---|---:|---|
| 1 | D.1 OpenAPI | ChatGPT GPT-5.6 Luna | Membuat draft OpenAPI 3.0 berdasarkan LLD, user stories, stack FastAPI, database, serta aturan endpoint dan AI. | 4 | Menyesuaikan endpoint agar tidak ada endpoint di luar LLD; menyelaraskan response/error code; menambahkan Bearer JWT dan respons timeout AI. |
| 2 | D.2 ERD/Skema | ChatGPT GPT-5.6 Luna | Membuat ERD Mermaid dan skema Pydantic berdasarkan OpenAPI hasil revisi serta struktur entitas LLD. | 5 | Menyelaraskan nama field, relasi FK, enum status, nullable field, confidence 0-1, dan struktur demand_forecasts. |
| 3 | Iterasi lanjutan | ChatGPT GPT-5.6 Luna | Sinkronisasi akhir antara OpenAPI dan ERD serta pengecekan deliverable PTM-05. | 5 | Memastikan daftar endpoint final sama dengan LLD dan menghapus endpoint tambahan yang tidak diminta. |

## Catatan penggunaan AI

AI digunakan sebagai co-pilot untuk penyusunan draft kontrak API, ERD, dan skema validasi. Hasil tetap direview dan disesuaikan dengan LLD, user stories, acceptance criteria, serta ERD proyek.

## Asumsi

Versi final mengikuti struktur ERD yang telah ditetapkan. Tidak ada asumsi tambahan yang perlu dicatat untuk field utama.
