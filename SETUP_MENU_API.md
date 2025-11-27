# Menu Catalog API - Setup Guide

## Prerequisites
- Python 3.11+
- PostgreSQL (via Laragon atau standalone)
- pip untuk package management

## Setup Instructions

### 1. Install Dependencies

```powershell
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
venv\Scripts\Activate.ps1

# Install dependencies
pip install -e ".[dev]"
```

### 2. Setup Database

Pastikan PostgreSQL di Laragon sudah running, lalu:

1. Buat database baru dengan nama `app`:
   - Buka pgAdmin atau HeidiSQL dari Laragon
   - Create database: `app`

2. Update file `.env` jika perlu:
   ```env
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/app
   ```

### 3. Run Application

```powershell
# Pastikan virtual environment aktif
venv\Scripts\Activate.ps1

# Run aplikasi
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

Aplikasi akan berjalan di: `http://localhost:8080`

### 4. Access Documentation

- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc

## API Endpoints

### Menu Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/menu` | Create new menu item |
| GET | `/api/menu` | List all menu items (with filters & pagination) |
| GET | `/api/menu/{id}` | Get menu item by ID |
| PUT | `/api/menu/{id}` | Full update menu item |
| DELETE | `/api/menu/{id}` | Delete menu item |
| GET | `/api/menu/group-by-category` | Group menu items by category |
| GET | `/api/menu/search` | Search menu items (convenience endpoint) |

### Query Parameters for GET /menu

- `q`: Search in name, description, ingredients
- `category`: Filter by category
- `min_price`: Minimum price filter
- `max_price`: Maximum price filter
- `max_cal`: Maximum calories filter
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 10, max: 100)
- `sort`: Sort by field:order (e.g., `price:asc`, `name:desc`)

### Example Request - Create Menu

```json
POST /api/menu
{
  "name": "Es Kopi Susu",
  "category": "drinks",
  "calories": 180,
  "price": 25000.00,
  "ingredients": ["coffee", "milk", "ice", "sugar"],
  "description": "Classic iced coffee with milk"
}
```

### Example Request - List Menu with Filters

```
GET /api/menu?category=drinks&max_price=30000&page=1&per_page=10&sort=price:asc
```

## Testing with Postman

1. Import collection: `gdgoc-studycase-postman.json`
2. Set variable `BASE_URL` to: `http://localhost:8080/api`
3. Run the collection

## Database Schema

### Menu Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| name | VARCHAR(255) | Menu item name |
| category | VARCHAR(100) | Category (drinks, food, etc.) |
| calories | FLOAT | Calorie content |
| price | FLOAT | Price in IDR |
| ingredients | JSON | Array of ingredients |
| description | TEXT | Description |
| created_at | DATETIME | Creation timestamp |
| updated_at | DATETIME | Last update timestamp |

## Troubleshooting

### Database Connection Error

Pastikan:
1. PostgreSQL service running (cek di Laragon)
2. Database `app` sudah dibuat
3. Credentials di `.env` benar
4. Port 5432 tidak digunakan aplikasi lain

### Import Error

```powershell
# Pastikan PYTHONPATH diset
$env:PYTHONPATH = "app"
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

## Development Notes

- Database tables akan dibuat otomatis saat aplikasi start (via SQLAlchemy)
- Logging tersedia via loguru
- Request/Response validation via Pydantic
- API documentation auto-generated via FastAPI
