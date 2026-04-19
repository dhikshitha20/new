# TaskFlow — FastAPI Task Manager

A full-stack Task Manager with a FastAPI backend and vanilla HTML/JS/CSS frontend.

🔗 Live: https://new-1-zgyr.onrender.com  
📖 API Docs: https://new-1-zgyr.onrender.com/docs

---

## Features

- JWT authentication (register, login, logout)
- Full task CRUD (create, read, update, delete)
- Mark tasks complete / incomplete
- Filter by status (?completed=true/false)
- Pagination (10 tasks per page)
- Password hashing with bcrypt
- SQLite (default) or PostgreSQL support
- 11 pytest test cases
- Docker + Docker Compose support
- Responsive single-page frontend

---

## Project Structure
├── main.py           # FastAPI app entry point + frontend serving
├── auth.py           # Register & login routes
├── tasks.py          # Task CRUD routes
├── models.py         # SQLAlchemy ORM models
├── schemas.py        # Pydantic schemas
├── database.py       # DB session setup
├── config.py         # Settings via pydantic-settings
├── security.py       # Password hashing
├── dependencies.py   # JWT creation & auth dependency
├── test_api.py       # pytest test suite
├── index.html        # Frontend single-page app
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md

---

## Environment Variables

Copy `.env.example` to `.env` and fill in:

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | (required) | JWT signing secret |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Token lifetime in minutes |
| `DATABASE_URL` | `sqlite:///./taskmanager.db` | DB connection string |

**Never commit `.env` to version control.**

---

## Running Locally

### Option 1 — Docker Compose

```bash
git clone https://github.com/dhikshitha20/new.git
cd new
cp .env.example .env
# Edit .env and set SECRET_KEY
docker compose up --build
```

Visit http://localhost:8000

### Option 2 — Manual

```bash
git clone https://github.com/dhikshitha20/new.git
cd new

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# Edit .env and set SECRET_KEY

uvicorn main:app --reload --port 8000
```

Visit http://localhost:8000

---

## Running Tests

```bash
pip install -r requirements.txt
pytest test_api.py -v
```

---

## API Endpoints

### Auth

| Method | Path | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and receive JWT |

### Tasks (require `Authorization: Bearer <token>`)

| Method | Path | Description |
|---|---|---|
| POST | `/tasks` | Create a task |
| GET | `/tasks` | List tasks (paginated, filterable) |
| GET | `/tasks/{id}` | Get a specific task |
| PUT | `/tasks/{id}` | Update title / description / completed |
| DELETE | `/tasks/{id}` | Delete a task |

**Query params for `GET /tasks`:**

| Param | Type | Description |
|---|---|---|
| `page` | int | Page number (default: 1) |
| `page_size` | int | Items per page (default: 10, max: 100) |
| `completed` | bool | Filter by completion status |