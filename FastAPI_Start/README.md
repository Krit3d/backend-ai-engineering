# 🚀 Core API Service (FastAPI)

This module serves as the foundational backend architecture for future AI-agent integration and data orchestration. It is built with a focus on true asynchrony, modularity, and strict data validation, utilizing the Repository pattern for clean architecture.

## ⚙️ Tech Stack
- **Framework:** FastAPI
- **Database:** PostgreSQL (via `asyncpg` for high-performance non-blocking I/O)
- **ORM & Migrations:** SQLAlchemy 2.0 (asyncio) & Alembic
- **Validation:** Pydantic V2 (`pydantic-settings` for configuration)
- **Server:** Uvicorn
- **Containerization:** Docker & Docker Compose

## 🏗️ Architectural Highlights
- **Repository Pattern:** Database logic is strictly decoupled from HTTP routers, making the codebase easier to maintain, test, and scale.
- **Asynchronous ORM:** Fully asynchronous database interactions using SQLAlchemy 2.0 and the `asyncpg` driver.
- **Automated Migrations:** Database schema changes are version-controlled and applied via Alembic.
- **Environment Management:** Sensitive data and configurations (like DB credentials) are securely managed via `.env` files and a dedicated `config.py` module. Dynamic DB URL generation is used to keep `alembic.ini` clean.

## 📂 Project Structure
```text
FastAPI_Start/
│
├── app/
│   ├── alembic/            # Database migration scripts and env
│   ├── repositories/       # DB interaction logic (Repository Pattern)
│   ├── routers/            # API endpoints (GET, POST)
│   ├── schemas/            # Pydantic validation models
│   ├── config.py           # Environment variables validation
│   ├── database.py         # Async engine & session management
│   ├── main.py             # FastAPI app init
│   └── models.py           # SQLAlchemy declarative base and tables
│
├── .dockerignore           # Docker build exclusions
├── .env                    # Local env vars (DB credentials)
├── alembic.ini             # Alembic configuration
├── docker-compose.yml      # API & PostgreSQL orchestration
├── Dockerfile              # Container setup
├── README.md               # Local documentation
└── requirements.txt        # Python dependencies
```

## 🛠️ Quick Start
To run this app, ensure you have installed Docker Desktop or the Docker Engine.

**1. Clone the repository and navigate to the project directory:**
```bash
git clone https://github.com/Krit3d/backend-ai-engineering.git
cd FastAPI_Start
```

**2. Configure Environment Variables:**
Create a `.env` file in the root of the `FastAPI_Start` directory and configure your database credentials (ensure they match your `docker-compose.yml` configuration):
```env
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=fastapi_db
```

**3. Build and run the containers:**
```bash
docker-compose up -d --build
```

**4. Apply Database Migrations:**
Once the containers are running, execute Alembic inside the backend container to create the tables:
```bash
docker compose exec backend alembic upgrade head
```
(Note: Replace backend with the actual name of your API service in docker-compose.yml if different).

## 📡 API Documentation
Once the server is running, FastAPI automatically generates interactive API documentation.
- **Swagger UI:** Navigate to `http://127.0.0.1:8000/docs` in your browser to test endpoints directly.
- **ReDoc:** Navigate to `http://127.0.0.1:8000/redoc` for alternative documentation formatting.