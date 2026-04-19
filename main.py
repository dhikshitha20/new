from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from database import Base, engine
import models
import auth
import tasks

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description="A simple task management API with JWT authentication.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(tasks.router)

@app.get("/", include_in_schema=False)
def serve_frontend():
    return FileResponse("index.html")

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "message": "Task Manager API is running"}