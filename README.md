# TaskFlow — FastAPI Task Manager

A full-stack Task Manager with a FastAPI backend and a vanilla HTML/JS/CSS frontend.

---

## Features

- JWT authentication (register, login, logout)
- Full task CRUD (create, read, update, delete)
- Mark tasks complete / incomplete
- Filter by status (all / pending / completed)
- Pagination (10 tasks per page)
- Password hashing with bcrypt
- SQLite (default) or PostgreSQL support
- Pytest test suite (11 tests)
- Docker + Docker Compose support

---

## Project Structure

```
taskmanager/
├── backend/
│   ├── app/
│   │   ├── core/           # config, security, dependencies
│   │   ├── db/             # database session
│   │   ├── models/         # SQLAlchemy ORM models
│   │   ├── routers/        # auth & tasks endpoints
│   │   ├── schemas/        # Pydantic schemas
│   │   └── main.py         # FastAPI app entry point
│   ├── tests/
│   │   └── test_api.py     # pytest test suite
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── index.html          # Single-page app
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## Environment Variables

Copy `backend/.env.example` to `backend/.env` and fill in:

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | (required) | JWT signing secret — use a long random string |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Token lifetime |
| `DATABASE_URL` | `sqlite:///./taskmanager.db` | DB connection string |

**Never commit `.env` to version control.**

---

## Running Locally

### Option 1 — Docker Compose (recommended)

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/taskmanager.git
cd taskmanager

# Create backend/.env from example
cp backend/.env.example backend/.env
# Edit backend/.env and set SECRET_KEY

# Build and start
docker compose up --build
```

- Frontend: http://localhost:3000  
- API docs: http://localhost:8000/docs

---

### Option 2 — Manual (no Docker)

**Backend**

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and set SECRET_KEY

# Run the server
uvicorn app.main:app --reload --port 8000
```

**Frontend**

Open `frontend/index.html` directly in your browser.  
The app points to `http://localhost:8000` by default when running locally.

---

## Running Tests

```bash
cd backend
pip install -r requirements.txt
pytest tests/ -v
```

---

## API Endpoints

### Authentication

| Method | Path | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and receive JWT |

### Tasks (all require `Authorization: Bearer <token>`)

| Method | Path | Description |
|---|---|---|
| POST | `/tasks` | Create a task |
| GET | `/tasks` | List tasks (paginated, filterable) |
| GET | `/tasks/{id}` | Get a specific task |
| PUT | `/tasks/{id}` | Update title / description / completed |
| DELETE | `/tasks/{id}` | Delete a task |

**Query parameters for `GET /tasks`:**

| Param | Type | Description |
|---|---|---|
| `page` | int | Page number (default: 1) |
| `page_size` | int | Items per page (default: 10, max: 100) |
| `completed` | bool | Filter by completion status |

Interactive docs are available at `/docs` (Swagger UI).

---

## Deployment (Render)

### Backend

1. Create a new **Web Service** on [Render](https://render.com)
2. Set **Root Directory** to `backend`
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables: `SECRET_KEY`, `DATABASE_URL`

### Frontend

1. Create a new **Static Site** on Render
2. Set **Root Directory** to `frontend`
3. Publish directory: `.` (or `frontend`)
4. Update the `API` constant in `frontend/index.html` to your backend URL

---

## Live Demo

🔗 [https://your-deployment-url.onrender.com](https://your-deployment-url.onrender.com)  
📖 API docs: [https://your-backend-url.onrender.com/docs](https://your-backend-url.onrender.com/docs)
