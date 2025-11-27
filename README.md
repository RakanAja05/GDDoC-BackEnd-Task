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
    ├── core                - application configuration, startup events, logging.
    ├── models              - pydantic models for this application.
    ├── services            - logic that is not just crud related.
    ├── main-aws-lambda.py  - [Optional] FastAPI application for AWS Lambda creation and configuration.
    └── main.py             - FastAPI application creation and configuration.
    |
    | # ML stuff
    ├── data             - where you persist data locally
    │   ├── interim      - intermediate data that has been transformed.
    │   ├── processed    - the final, canonical data sets for modeling.
    │   └── raw          - the original, immutable data dump.
    │
    ├── notebooks        - Jupyter notebooks. Naming convention is a number (for ordering),
    |
    ├── ml               - modelling source code for use in this project.
    │   ├── __init__.py  - makes ml a Python module
    │   ├── pipeline.py  - scripts to orchestrate the whole pipeline
    │   │
    │   ├── data         - scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features     - scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   └── model        - scripts to train models and make predictions
    │       ├── predict_model.py
    │       └── train_model.py
    │
    └── tests            - pytest

## GCP

Deploying inference service to Cloud Run

### Authenticate

1. Install `gcloud` cli
2. `gcloud auth login`
3. `gcloud config set project <PROJECT_ID>`

### Enable APIs

1. Cloud Run API
2. Cloud Build API
3. IAM API

### Deploy to Cloud Run

1. Run `gcp-deploy.sh`

### Clean up

1. Delete Cloud Run
2. Delete Docker image in GCR

## AWS

Deploying inference service to AWS Lambda

### Authenticate

1. Install `awscli` and `sam-cli`
2. `aws configure`

### Deploy to Lambda

1. Run `sam build`
2. Run `sam deploy --guiChange this portion for other types of models

## Add the correct type hinting when completed

`aws cloudformation delete-stack --stack-name <STACK_NAME_ON_CREATION>`

Made by <https://github.com/arthurhenrique/cookiecutter-fastapi/graphs/contributors> with ❤️
