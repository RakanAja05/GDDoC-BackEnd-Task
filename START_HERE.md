# 🚀 START HERE - Menu Catalog API

> **Project**: GDGoC Study Case - Menu Catalog Backend API
> **Status**: ✅ Ready to Run
> **Setup Time**: 5-10 minutes

---

## 📌 Apa yang Sudah Dibuat?

Project ini sekarang memiliki **Menu Catalog API** yang lengkap dengan:

✅ **CRUD Operations** - Create, Read, Update, Delete menu items
✅ **Search & Filter** - Cari menu berdasarkan nama, kategori, harga, kalori
✅ **Pagination** - List menu dengan pagination otomatis
✅ **Sorting** - Urutkan berdasarkan field apa saja
✅ **Group by Category** - Kelompokkan menu per kategori
✅ **PostgreSQL Database** - Database yang robust dan scalable
✅ **Auto Documentation** - Swagger UI & ReDoc built-in
✅ **Sample Data** - 8 menu items siap pakai
✅ **Unit Tests** - Test coverage untuk semua endpoint
✅ **Postman Collection** - Siap import dan test

---

## 🎯 Quick Start (5 Menit)

### 1. Install Dependencies (2 menit)
```powershell
# Buat virtual environment
python -m venv venv

# Aktifkan
.\venv\Scripts\Activate.ps1

# Install packages
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic loguru requests httpx joblib scikit-learn pandas pytest
```

### 2. Setup Database (1 menit)
```powershell
# Di Laragon: Start PostgreSQL
# Buat database bernama 'app'
# (via HeidiSQL atau pgAdmin)
```

### 3. Initialize Database (1 menit)
```powershell
# Run setup script
python setup_db.py
```

Output yang diharapkan:
```
✅ Database connection successful!
✅ Tables created successfully!
✅ Inserted 8 sample menu items!
✅ Setup completed successfully!
```

### 4. Run Application (1 menit)
```powershell
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### 5. Test! 🎉
Buka browser: **http://localhost:8080/docs**

---

## 📚 Dokumentasi

| File | Isi |
|------|-----|
| **[QUICK_START.md](QUICK_START.md)** | 📘 Setup guide lengkap + troubleshooting |
| **[SETUP_MENU_API.md](SETUP_MENU_API.md)** | 📗 API documentation lengkap |
| **[SUMMARY.md](SUMMARY.md)** | 📙 Technical implementation details |
| **[CHECKLIST.md](CHECKLIST.md)** | ✅ Compliance checklist |
| **[README.md](README.md)** | 📖 Project overview |

**Baca salah satu sesuai kebutuhan!**

---

## 🔌 API Endpoints yang Tersedia

### Menu Catalog API (NEW ✨)

```
POST   /api/menu                      → Create menu
GET    /api/menu                      → List all (with filters)
GET    /api/menu/{id}                 → Get by ID
PUT    /api/menu/{id}                 → Update menu
DELETE /api/menu/{id}                 → Delete menu
GET    /api/menu/group-by-category    → Group by category
GET    /api/menu/search               → Search menu
```

### ML Prediction API (Existing)

```
POST   /api/v1/predict                → Make prediction
GET    /api/v1/health                 → Health check
```

---

## 🧪 Testing

### Option 1: Swagger UI (Recommended untuk mulai)
1. Run aplikasi
2. Buka: http://localhost:8080/docs
3. Coba endpoint langsung dari browser

### Option 2: Postman
1. Import: `gdgoc-studycase-postman.json`
2. Set variable `BASE_URL`: `http://localhost:8080/api`
3. Run collection → **All tests should pass ✅**

### Option 3: Unit Tests
```powershell
pytest tests/test_menu_api.py -v
```

---

## 💡 Example Usage

### Create Menu
```bash
curl -X POST http://localhost:8080/api/menu \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Es Teh Manis",
    "category": "drinks",
    "calories": 90,
    "price": 15000,
    "ingredients": ["tea", "sugar", "ice"],
    "description": "Sweet iced tea"
  }'
```

### Search Menu
```bash
curl "http://localhost:8080/api/menu?q=kopi&max_price=30000&sort=price:asc"
```

### Get All Menus
```bash
curl http://localhost:8080/api/menu
```

---

## 🗂️ File Structure

```
📁 penugasan-gdgoc-be/
│
├── 📄 START_HERE.md          ← YOU ARE HERE
├── 📄 QUICK_START.md         ← Setup guide
├── 📄 SUMMARY.md             ← Implementation details
├── 📄 CHECKLIST.md           ← Compliance checklist
├── 📄 setup_db.py            ← Database setup script
│
├── 📁 app/
│   ├── 📁 models/
│   │   ├── menu.py           ✨ NEW - Menu model & schemas
│   │   ├── prediction.py
│   │   └── log.py
│   │
│   ├── 📁 api/routes/
│   │   ├── menu.py           ✨ NEW - Menu endpoints
│   │   ├── predictor.py
│   │   └── api.py            ✨ UPDATED - Added menu router
│   │
│   ├── 📁 core/
│   │   ├── config.py
│   │   ├── events.py
│   │   └── ...
│   │
│   ├── db.py
│   └── main.py
│
└── 📁 tests/
    └── test_menu_api.py      ✨ NEW - Unit tests
```

---

## ⚙️ Configuration

File `.env` sudah siap digunakan:

```env
SECRET_KEY=secret
DEBUG=True
MODEL_PATH=./ml/model/
MODEL_NAME=model.pkl
MEMOIZATION_FLAG=True
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/app
```

**Untuk Laragon, tidak perlu diubah!** ✅

---

## 🐛 Troubleshooting

### ❌ Error: Database connection failed
**Fix**: 
1. Cek PostgreSQL running di Laragon
2. Pastikan database `app` sudah dibuat
3. Cek username/password di `.env`

### ❌ Error: Module not found
**Fix**: 
1. Pastikan virtual environment aktif
2. Run: `pip install -e ".[dev]"`

### ❌ Error: Port 8080 already in use
**Fix**: 
1. Gunakan port lain: `--port 8081`
2. Atau stop aplikasi lain yang pakai port 8080

**Untuk troubleshooting lengkap, lihat [QUICK_START.md](QUICK_START.md)**

---

## ✅ Verification Checklist

Setelah setup, pastikan:

- [ ] Aplikasi running di http://localhost:8080
- [ ] Swagger docs bisa diakses di http://localhost:8080/docs
- [ ] Database `app` memiliki table `menus`
- [ ] Table `menus` memiliki 8 sample data
- [ ] Bisa create menu via Swagger UI
- [ ] Bisa list menu via browser
- [ ] Postman collection bisa import & run

---

## 🎉 Next Steps

1. ✅ **Setup** - Ikuti Quick Start di atas
2. 🧪 **Test** - Coba API via Swagger UI
3. 📝 **Read Docs** - Baca dokumentasi lengkap
4. 🚀 **Deploy** - (Optional) Deploy ke Cloud Run/Lambda

---

## 📞 Need Help?

- **Setup Issues**: Lihat [QUICK_START.md](QUICK_START.md)
- **API Usage**: Lihat [SETUP_MENU_API.md](SETUP_MENU_API.md)
- **Technical Details**: Lihat [SUMMARY.md](SUMMARY.md)
- **Swagger UI**: http://localhost:8080/docs (setelah running)

---

## 🎯 Summary

**Yang perlu dilakukan:**
1. Install dependencies (1 command)
2. Create database 'app' di PostgreSQL
3. Run `python setup_db.py`
4. Run aplikasi
5. Test via Swagger UI atau Postman

**Total waktu: 5-10 menit** ⏱️

**Happy coding! 🚀**

---

*Made with ❤️ for GDGoC Study Case*
