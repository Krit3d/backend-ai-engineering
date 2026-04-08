# 🚀 Core API Service (FastAPI)

This module serves as the foundational backend architecture for future AI-agent integration and data orchestration. It is built with a focus on true asynchrony, modularity, and strict data validation.

## ⚙️ Tech Stack
- **Framework:** FastAPI
- **Database:** SQLite (via `aiosqlite` for non-blocking I/O)
- **Validation:** Pydantic V2
- **Server:** Uvicorn

## 🏗️ Architectural Highlights
- **Separation of Concerns:** The application is strictly divided into routing (`routers/`), data validation (`schemas/`), and database connections (`database.py`).
- **Modular Routing:** Endpoints are managed via `APIRouter`, making the codebase scalable for future microservice expansion.
- **True Asynchrony:** Replaced standard blocking database calls with `aiosqlite`, ensuring the event loop remains unblocked during database transactions.

## 📂 Project Structure

```text
FastAPI_Start/
│
├── app/
│   ├── routers/
│   │   ├── __init__.py
│   │   └── users.py       # API endpoints (GET, POST)
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── users.py       # Pydantic models for request/response validation
│   ├── __init__.py
│   ├── database.py        # Async DB connection and raw SQL queries
│   └── main.py            # FastAPI application instance & router inclusion
│
└── requirements.txt
```

## 🛠️ Quick Start (Local Setup)

Follow these steps to run the API server locally:

**1. Navigate to the project directory:**
```bash
cd FastAPI_Start
```

**2. Create and activate a virtual environment:**
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/Mac:
source .venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Run the server:**
```bash
uvicorn app.main:app --reload
```

## 📡 API Documentation
Once the server is running, FastAPI automatically generates interactive API documentation.
- **Swagger UI:** Navigate to `http://127.0.0.1:8000/docs` in your browser to test endpoints directly.
- **ReDoc:** Navigate to `http://127.0.0.1:8000/redoc` for alternative documentation formatting.