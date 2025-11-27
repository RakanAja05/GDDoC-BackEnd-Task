# Penugasan-GDGoC-BE

Project for GDGoC recruitment - **FastAPI Backend Menu Catalog API with chat persona**

## 🎯 Features

### 1. Menu Catalog API 
- Full CRUD operations for menu management
- Advanced search & filtering
- Pagination & sorting
- Group by category
- PostgreSQL database integration

## 🚀 Quick Start

### Prerequisites
- Python 3.11+ 
- PostgreSQL (via Laragon or standalone)
- Virtual Environment

### Setup in 5 Minutes

```powershell
# 1. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic loguru requests httpx joblib scikit-learn pandas pytest

# 3. Setup database (create 'app' database in PostgreSQL first)
python setup_db.py

# 4. Run application
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

**📖 For detailed setup instructions, see [QUICK_START.md](QUICK_START.md)**

## 📚 Documentation

- **Quick Start**: [QUICK_START.md](QUICK_START.md) - 5-minute setup guide
- **Full Guide**: [SETUP_MENU_API.md](SETUP_MENU_API.md) - Complete documentation
- **Summary**: [SUMMARY.md](SUMMARY.md) - Implementation details
- **Swagger UI**: http://localhost:8080/docs (after running app)
- **ReDoc**: http://localhost:8080/redoc

## 🔌 API Endpoints

### Menu Catalog API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/menu` | Create menu item |
| GET | `/api/menu` | List menu items (with filters) |
| GET | `/api/menu/{id}` | Get menu by ID |
| PUT | `/api/menu/{id}` | Update menu item |
| DELETE | `/api/menu/{id}` | Delete menu item |
| GET | `/api/menu/group-by-category` | Group items by category |
| GET | `/api/menu/search` | Search menu items |


### Chat (Semantic) API — Gemini

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat` | Send a question to the semantic chat. Supports conversation tokens and persona role-play. Returns `{ reply, conversation_token }`.
| POST | `/api/conversations` | Create a new conversation token (returns `{ token }`). Frontend automatically creates one on first message.
| GET | `/api/conversations/{token}` | Fetch conversation history (messages with `role` and `content`).

Notes about the Chat feature:
- The app uses Google Generative AI (Gemini) to answer conversational questions. Set `GEMINI_API_KEY` in your `.env` to enable it.
- Persona: the chat will automatically use the `rakan` persona (first-person, relaxed, concise). The persona preset is defined in `app/services/personas.py` and used by the system prompt.
- Conversation tokens: when a user starts chatting, the frontend requests `POST /api/conversations` and stores the returned token in `localStorage` as `conversation_token`. Subsequent `/api/chat` calls send that token so the server persists and loads message history.
- Message persistence: user and assistant messages are saved in the `conversations` and `conversation_messages` tables using SQLAlchemy models in `app/models/conversation.py`.
- If your DB schema was created before these models, a helper script `scripts/fix_conversation_schema.py` can add the missing `content` column for SQLite.


## 📝 Example Usage

### Create Menu
```bash
curl -X POST http://localhost:8080/api/menu \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Es Kopi Susu",
    "category": "drinks",
    "calories": 180,
    "price": 25000,
    "ingredients": ["coffee", "milk", "ice"],
    "description": "Classic iced coffee"
  }'
```

### Search Menu
```bash
curl "http://localhost:8080/api/menu?q=kopi&category=drinks&max_price=30000&sort=price:asc"
```

## 🧪 Testing with Postman

1. Import collection: `gdgoc-studycase-postman.json`
2. Set variable `BASE_URL`: `http://localhost:8080/api`
3. Run the collection - all tests should pass ✅

## Development Requirements

- Python 3.11+
- PostgreSQL (Laragon recommended)
- pip or uv (Python Package Manager)

### Environment Variables (.env)

```env
SECRET_KEY=secret
DEBUG=True
MODEL_PATH=./ml/model/
MODEL_NAME=model.pkl
MEMOIZATION_FLAG=True
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/app
```

## Installation (Alternative with UV)

```sh
python -m venv venv
source venv/bin/activate
make install
```

## Runnning Localhost

`make run`

## Deploy app

`make deploy`

## Running Tests

`make test`

## Access Swagger Documentation

> <http://localhost:8080/docs>

## Access Redocs Documentation

> <http://localhost:8080/redoc>

## Project structure

Files related to application are in the `app` or `tests` directories.
Application parts are:

    app
    |
    | # Fast-API stuff
    ├── api                 - web related stuff.
    │   └── routes          - web routes.
    # Penugasan-GDGoC-BE

    Projek ini fokus pada dua fitur utama:
    - API Menu Catalog (CRUD, pencarian, filter, pagination)
    - Chat semantik berbasis Gemini dengan persona dan persistence konteks percakapan

    Tujuan README ini: menjelaskan cara menjalankan dan mencoba kedua fitur tersebut.

    ## Quick Start (singkat)

    Persyaratan singkat:
    - Python 3.11+
    - Database (untuk production gunakan PostgreSQL; lokal bisa memakai SQLite default)

    Menjalankan aplikasi secara lokal:

    ```powershell
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    python setup_db.py   # buat tabel & seed sample data (lokal)
    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
    ```

    Setelah berjalan, buka `http://localhost:8080/` untuk UI chat atau `http://localhost:8080/docs` untuk Swagger.

    ## Konfigurasi penting
    - `DATABASE_URL` — connection string untuk database. Default development: `sqlite:///./app.db`.
    - `GEMINI_API_KEY` — kunci API Google Generative AI (Gemini). Tanpa ini fitur chat semantik akan fallback ke pencarian sederhana.

    Letakkan env vars di file `.env` atau ekspor ke environment sebelum menjalankan server.

    ## Menu Catalog API

    Endpoint utama:

    | Method | Endpoint | Deskripsi |
    |--------|----------|-----------|
    | POST | `/api/menu` | Buat item menu |
    | GET  | `/api/menu` | List menu (support filter & pagination) |
    | GET  | `/api/menu/{id}` | Ambil menu berdasarkan ID |
    | PUT  | `/api/menu/{id}` | Update item menu |
    | DELETE | `/api/menu/{id}` | Hapus item menu |
    | GET | `/api/menu/group-by-category` | Kelompokkan item per kategori |
    | GET | `/api/menu/search` | Pencarian (normal + semantic when enabled) |

    Contoh membuat menu:

    ```bash
    curl -X POST http://localhost:8080/api/menu \
      -H "Content-Type: application/json" \
      -d '{"name":"Es Kopi Susu","category":"drinks","calories":180,"price":25000,"ingredients":["coffee","milk","ice"],"description":"Classic iced coffee"}'
    ```

    ## Chat (Semantic) — Gemini

    Fitur utama:
    - Chat semantik yang menggunakan Google Gemini untuk menghasilkan jawaban natural.
    - Persona: jawaban selalu menggunakan persona `rakan` (first-person, santai, ringkas).
    - Konteks percakapan: pesan disimpan di database; frontend menyimpan `conversation_token` di `localStorage` sehingga konteks dipertahankan antar request.

    Endpoints:

    | Method | Endpoint | Deskripsi |
    |--------|----------|-----------|
    | POST | `/api/chat` | Kirim pertanyaan ke chat. Payload JSON: `{ "question": "...", "conversation_token": "..." }`. Response: `{ "reply": "...", "conversation_token": "..." }` |
    | POST | `/api/conversations` | Buat conversation token baru (returns `{ token }`). Frontend otomatis membuat token saat sesi pertama.
    | GET  | `/api/conversations/{token}` | Ambil history pesan untuk token tertentu |

    Contoh: buat conversation token (opsional, frontend sudah membuat otomatis):

    ```bash
    curl -X POST http://localhost:8080/api/conversations
    ```

    Contoh: kirim pertanyaan ke chat (pakai token):

    ```bash
    curl -X POST http://localhost:8080/api/chat \
      -H "Content-Type: application/json" \
      -d '{"question":"Rekomendasi minuman dingin murah?","conversation_token":"<TOKEN_HERE>"}'
    ```

    Catatan penting:
    - Agar jawaban Gemini bekerja, set `GEMINI_API_KEY` di environment.
    - Pesan user dan assistant disimpan di tabel `conversations` dan `conversation_messages` (SQLAlchemy models `app/models/conversation.py`). Jika skema DB lama tidak punya kolom `content`, jalankan `scripts/fix_conversation_schema.py` untuk memperbaiki pada SQLite.

    ## Catatan singkat untuk penilai / reviewer
    - Fitur chat menunjukkan penggunaan LLM (Gemini) + prompt engineering (persona) dan persistence konteks percakapan.
    - Untuk deployment produksi, gunakan database terkelola (Postgres) dan konfigurasi `DATABASE_URL` di environment host — jangan gunakan SQLite file pada environment serverless.

    ## Jika ingin saya bantu lanjutkan
    - Tambah test automated untuk conversation/chat endpoints
    - Tambah Alembic migrations untuk model conversation
    - Siapkan Docker Compose dengan Postgres untuk CI / deployment

    ---
    Ringkas dan cukup untuk demo: buka `http://localhost:8080/`, mulai chat, dan coba `/api/menu/search` untuk pencarian semantic (set `GEMINI_API_KEY` terlebih dahulu).
