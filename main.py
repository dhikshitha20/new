from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
import models
import auth
import tasks
# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description="A simple task management API with JWT authentication.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(tasks.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Task Manager API is running"}
