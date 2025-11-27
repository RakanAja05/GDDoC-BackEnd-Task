# 🤖 Gemini AI Integration Guide

## ✅ Yang Sudah Disetup

1. ✅ Google Generative AI SDK installed
2. ✅ Gemini service (`app/services/gemini_search.py`)
3. ✅ Search endpoint integrated dengan Gemini
4. ✅ Fallback ke simple search jika API key tidak ada

---

## 🔑 Cara Mendapatkan Gemini API Key

### 1. Buka Google AI Studio
Kunjungi: https://makersuite.google.com/app/apikey

### 2. Sign in dengan Google Account

### 3. Create API Key
- Klik **"Get API Key"** atau **"Create API Key"**
- Pilih project atau buat baru
- Copy API key yang dihasilkan

### 4. Update `.env` File
```env
GEMINI_API_KEY=AIzaSyC_your_actual_api_key_here
```

---

## 🚀 Cara Testing

### 1. Restart Aplikasi
```powershell
# Stop aplikasi (Ctrl+C)
# Start lagi
$env:PYTHONPATH="$pwd\app"
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### 2. Test Semantic Search

#### Via Browser/Postman:
```
GET http://localhost:8080/api/menu/search?q=minuman dingin murah
GET http://localhost:8080/api/menu/search?q=makanan tinggi kalori
GET http://localhost:8080/api/menu/search?q=menu dibawah 25 ribu
GET http://localhost:8080/api/menu/search?q=kopi dengan susu
```

#### Via curl:
```bash
curl "http://localhost:8080/api/menu/search?q=minuman+manis"
```

---

## 🎯 Contoh Natural Language Queries

Gemini AI akan parse query ini menjadi filter database:

| Query | Hasil Parse |
|-------|-------------|
| "minuman murah dibawah 20 ribu" | `category: drinks, max_price: 20000` |
| "makanan tinggi kalori" | `category: food, keywords: ["kalori", "tinggi"]` |
| "kopi dengan susu" | `keywords: ["kopi", "susu"]` |
| "menu rendah kalori" | `max_calories: 200` |
| "es teh manis" | `keywords: ["es", "teh", "manis"]` |

---

## 📊 Flow Diagram

```
User Query
    ↓
Search Endpoint (/menu/search?q=...)
    ↓
Gemini Service
    ├─ Parse query → Extract filters
    └─ If no API key → Simple keyword search
    ↓
Filter Menu Items
    ├─ Category filter
    ├─ Price range filter
    ├─ Calories filter
    └─ Keyword matching
    ↓
Return Paginated Results
```

---

## ⚙️ Configuration

### `.env` Variables
```env
# Gemini API Key (required for semantic search)
GEMINI_API_KEY=your_api_key_here
```

### `app/core/config.py`
```python
GEMINI_API_KEY: str = config("GEMINI_API_KEY", default="")
```

---

## 🔧 Fallback Behavior

Jika API key **tidak ada** atau **invalid**:
- ✅ Aplikasi tetap jalan
- ✅ Search endpoint tetap work
- ✅ Menggunakan simple keyword search
- ⚠️ Log warning: "Gemini API key not configured"

---

## 🧪 Testing dengan Postman

### Test 1: Simple Search
```
GET {{BASE_URL}}/menu/search?q=kopi&page=1&per_page=10
```

Expected: Menu items yang mengandung kata "kopi"

### Test 2: Natural Language
```
GET {{BASE_URL}}/menu/search?q=minuman murah dibawah 25000&page=1&per_page=10
```

Expected: Drinks dengan price ≤ 25000

### Test 3: Complex Query
```
GET {{BASE_URL}}/menu/search?q=makanan tinggi kalori diatas 400&page=1&per_page=10
```

Expected: Food items dengan calories > 400

---

## 📝 Response Format

```json
{
  "data": [
    {
      "id": 1,
      "name": "Es Kopi Susu",
      "category": "drinks",
      "calories": 180,
      "price": 25000,
      "ingredients": ["coffee", "milk", "ice", "sugar"],
      "description": "Classic iced coffee with milk",
      "created_at": "2025-11-26T...",
      "updated_at": "2025-11-26T..."
    }
  ],
  "pagination": {
    "total": 3,
    "page": 1,
    "per_page": 10,
    "total_pages": 1
  }
}
```

---

## 🐛 Troubleshooting

### Error: "Gemini API key not configured"
**Fix**: Tambahkan API key di `.env` dan restart aplikasi

### Error: "API key invalid"
**Fix**: 
1. Cek API key di Google AI Studio
2. Pastikan tidak ada spaces atau karakter extra
3. Generate API key baru jika perlu

### Search tidak akurat
**Fix**: 
- Tambah sample menu di `_get_menu_sample()` untuk context lebih baik
- Adjust prompt di `parse_search_query()` method

---

## 🎉 Next Steps

1. ✅ Get Gemini API key dari Google AI Studio
2. ✅ Update `.env` dengan API key
3. ✅ Restart aplikasi
4. ✅ Test dengan natural language queries
5. ✅ Check logs untuk melihat parsing results

**Happy searching! 🚀**
