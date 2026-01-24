# FastAPI User Management API

This project is a **FastAPI** application with PostgreSQL that supports:

* Multiple roles (`admin`, `backoffice`, `agent`)
* User authentication with **JWT access and refresh tokens**
* User login, logout, refresh tokens
* Protected routes (`/me`)
* Global token storage in database
* Logging and error handling

---

## 📦 Prerequisites

* Python 3.10+
* PostgreSQL (or Docker)
* Git

---

## ⚡ Installation (Local)

1. Clone the repository:

```bash
git clone <repo-url>
cd <repo-folder>
```

2. Create and activate Python virtual environment:

```bash
python -m venv venv
# Windows
.\venv\Scripts\Activate
# Mac/Linux
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up `.env` file in project root:

```env
DATABASE_URL=postgresql://postgres:@127.0.0.1:5432/sidago_crm
SECRET_KEY=supersecretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
```

5. Run database migrations / create tables (if not using Alembic, ensure models are created):

```bash
python
>>> from database.db import Base, engine
>>> Base.metadata.create_all(bind=engine)
>>> exit()
```

6. Seed the database with initial users:

```bash
python -m seeders.user
```

---

## 🚀 Running the API (Local)

```bash
uvicorn main:app --reload
```

API will run at:

```
http://127.0.0.1:8000
```

Swagger docs are available at:

```
http://127.0.0.1:8000/docs
```

---

## 🗃️ Pre-seeded Users

| Email                                                     | Username    | Roles      | Password    |
| --------------------------------------------------------- | ----------- | ---------- | ----------- |
| [admin1@example.com](mailto:admin1@example.com)           | admin1      | admin      | password123 |
| [admin2@example.com](mailto:admin2@example.com)           | admin2      | admin      | password123 |
| [admin3@example.com](mailto:admin3@example.com)           | admin3      | admin      | password123 |
| [backoffice1@example.com](mailto:backoffice1@example.com) | backoffice1 | backoffice | password123 |
| [backoffice2@example.com](mailto:backoffice2@example.com) | backoffice2 | backoffice | password123 |
| [backoffice3@example.com](mailto:backoffice3@example.com) | backoffice3 | backoffice | password123 |
| [agent1@example.com](mailto:agent1@example.com)           | agent1      | agent      | password123 |
| [agent2@example.com](mailto:agent2@example.com)           | agent2      | agent      | password123 |
| [agent3@example.com](mailto:agent3@example.com)           | agent3      | agent      | password123 |

---

## 🐳 Running with Docker

1. Make sure `Docker` and `docker-compose` are installed.

2. Build and start containers:

```bash
docker-compose up --build
```

3. API will be accessible at:

```
http://localhost:8000
```

Swagger docs:

```
http://localhost:8000/docs
```

4. Seed database in Docker:

```bash
docker-compose exec sidago_crm python -m seeders.user
```

---

## 📝 API Endpoints

| Method | Endpoint | Description                         |
| ------ | -------- | ----------------------------------- |
| POST   | /login   | Login with email & password         |
| POST   | /logout  | Logout user (requires access token) |
| POST   | /refresh | Refresh access & refresh tokens     |
| GET    | /me      | Get current logged-in user info     |

---

This README ensures **both local development and Docker usage** are covered, along with instructions for **seeding the initial users**.
