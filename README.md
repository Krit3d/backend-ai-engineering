# 🚀 Backend Microservices & AI Integration

Welcome! This mono-repository contains a collection of microservices, data extraction tools, and APIs. It serves as the foundational infrastructure for future AI-agent orchestration and LLM tool-calling.

### 🛠️ Tech Stack & Tools

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![FastAPI](https://img.shields.io/badge/fastapi-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)

### 📁 Projects in this Repository

**Every project here contains his own README with setup instructions.**
| Project | Description | Stack | Status |
| :--- | :--- | :--- | :--- |
| [**🚀 FastAPI (CORE)**](./FastAPI_Start) | Asynchronous API with Pydantic validation, Repository pattern, SQLAlchemy 2.0 ORM, Alembic migrations, and Docker containerization. | `FastAPI`, `asyncpg`, `PostgreSQL`, `Docker` | Active Development |
| [**🤖 TG_Bot**](./TG_Bot) | An asynchronous Telegram bot with external API integration (CoinGecko) and SQLite DB for user management. | `aiogram 3`, `aiohttp`, `sqlite3` | Completed |
| [**🕷️ Parser**](./Parser) | Web scraping tool for extracting structured data. | `BeautifulSoup4`, `requests` | Completed |
| [**📡 API_Scout**](./API_Scout) | A lightweight script for testing and fetching data from public APIs. | `requests`, `JSON` | Completed |

### 🗺️ Architecture Evolution
- [x] **Phase 1: Simple API Data Fetching.** Basic Python, `requests` library for public API data retrieval (`API_Scout`).
- [x] **Phase 2: Web Scraping.** Data extraction from websites using `BeautifulSoup4`, text parsing, and structuring (`Parser`).
- [x] **Phase 3: Async Bot & Persistence.** Asynchronous programming with `asyncio` and `aiohttp`, Telegram Bot integration, and SQLite database for user management (`TG_Bot`).
- [x] **Phase 4: Backend & Persistence.** FastAPI, PostgreSQL, Async ORM (SQLAlchemy 2.0), Migrations (Alembic), Dockerization.
- [/] **Phase 5: AI Integration.** Building RAG pipelines, AI-agent orchestration, and LLM tool-calling. (Current)

---

_Currently focused on building AI-integrated backend systems. Open to networking and engineering opportunities._

_Feel free to reach out to me on [LinkedIn](www.linkedin.com/in/kirill-kshenyov-1667843b4)._

_TG_: **@kshenyovsu**
