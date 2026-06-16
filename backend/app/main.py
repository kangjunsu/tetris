from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import engine, Base
from .routers import auth, users, games

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Tetris Game API",
    description="Backend API for Tetris game with user authentication and leaderboard",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(games.router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "message": "Tetris Game API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
