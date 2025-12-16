"""
SautiNa - Multilingual Voice-First AI Assistant
FastAPI backend for Nigerian language voice assistant.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from config import settings
from api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - setup and teardown"""
    # Create temp directory for audio files
    os.makedirs(settings.temp_dir, exist_ok=True)
    print(f"🎤 SautiNa starting...")
    print(f"📡 N-ATLaS endpoint: {settings.natlas_api_url}")
    yield
    # Cleanup on shutdown
    print("👋 SautiNa shutting down...")


app = FastAPI(
    title=settings.app_name,
    description="Multilingual, voice-first AI assistant for Nigerian users. "
                "Supports Hausa, Yoruba, Igbo, and Nigerian Pidgin.",
    version=settings.app_version,
    lifespan=lifespan,
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for hackathon
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for audio responses
os.makedirs(settings.temp_dir, exist_ok=True)
app.mount("/audio", StaticFiles(directory=settings.temp_dir), name="audio")

# Include API routes
app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint with welcome message"""
    return {
        "message": "Welcome to SautiNa! 🇳🇬",
        "description": "Multilingual voice assistant for Nigerian users",
        "languages": ["Hausa", "Yoruba", "Igbo", "Nigerian Pidgin", "English"],
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
