# Quick Start - Menu Catalog API

## 🚀 Setup Cepat (5 Menit)

### 1️⃣ Install Dependencies
```powershell
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic loguru requests httpx joblib scikit-learn pandas pytest
```

### 2️⃣ Setup Database PostgreSQL di Laragon

1. Start PostgreSQL dari Laragon
2. Buka HeidiSQL/pgAdmin
3. Buat database baru: **`app`**
4. Update `.env`:
   ```env
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/app
   ```

### 3️⃣ Setup Database & Sample Data
```powershell
python setup_db.py
```

Output yang diharapkan:
```
✅ Database connection successful!
✅ Tables created successfully!
✅ Inserted 8 sample menu items!
```

### 4️⃣ Run Aplikasi
```powershell
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### 5️⃣ Test API
Buka browser: **http://localhost:8080/docs**

---

## 📝 Test dengan Postman

1. Import file: `gdgoc-studycase-postman.json`
2. Set variable `BASE_URL`: `http://localhost:8080/api`
3. Run collection

---

## 🎯 Endpoints Utama

### Create Menu
```http
POST http://localhost:8080/api/menu
Content-Type: application/json

{
  "name": "Es Teh Manis",
  "category": "drinks",
  "calories": 90,
  "price": 15000.00,
  "ingredients": ["tea", "sugar", "ice"],
  "description": "Sweet iced tea"
}
```

### Get All Menu
```http
GET http://localhost:8080/api/menu
```

### Get Menu by ID
```http
GET http://localhost:8080/api/menu/1
```

### Search Menu
```http
GET http://localhost:8080/api/menu?q=kopi&category=drinks&max_price=30000&sort=price:asc
```

### Group by Category
```http
GET http://localhost:8080/api/menu/group-by-category?mode=count
GET http://localhost:8080/api/menu/group-by-category?mode=list&per_category=5
```

### Update Menu
```http
PUT http://localhost:8080/api/menu/1
Content-Type: application/json

{
  "name": "Es Kopi Susu Premium",
  "category": "drinks",
  "calories": 190,
  "price": 30000.00,
  "ingredients": ["coffee", "milk", "ice", "condensed_milk"],
  "description": "Premium iced coffee"
}
```

### Delete Menu
```http
DELETE http://localhost:8080/api/menu/1
```

---

## ✅ Verifikasi

Setelah setup, cek:

1. ✅ Aplikasi running di http://localhost:8080
2. ✅ Swagger docs tersedia di http://localhost:8080/docs
3. ✅ Database `app` memiliki table `menus`
4. ✅ Table `menus` memiliki 8 sample data
5. ✅ Postman collection bisa run semua tests

---

## 🐛 Troubleshooting

### Error: `could not connect to server`
- Cek PostgreSQL running di Laragon
- Cek port 5432 tidak digunakan aplikasi lain

### Error: `relation "menus" does not exist`
- Run `python setup_db.py` untuk create tables

### Error: `Import "sqlalchemy" could not be resolved`
- Pastikan virtual environment aktif: `.\venv\Scripts\Activate.ps1`
- Install dependencies: `pip install -e ".[dev]"`

### Error: `No module named 'app'`
- Set PYTHONPATH: `$env:PYTHONPATH = "app"`
- Atau run dengan: `python -m uvicorn app.main:app --reload`

---

## 📂 File Structure

```
app/
├── models/
│   ├── menu.py          # ✨ NEW: Menu model & schemas
│   ├── prediction.py    # Existing ML models
│   └── log.py          # Request logging
├── api/
│   └── routes/
│       ├── menu.py      # ✨ NEW: Menu endpoints
│       ├── predictor.py # Existing ML endpoint
│       └── api.py       # Router aggregator (updated)
├── core/
│   ├── config.py
│   ├── events.py        # Database initialization
│   └── ...
└── main.py             # FastAPI app

setup_db.py              # ✨ NEW: Database setup script
SETUP_MENU_API.md       # ✨ NEW: Full documentation
QUICK_START.md          # ✨ NEW: This file
```

---

## 🎉 Selesai!

Aplikasi Menu Catalog API sudah siap digunakan!
