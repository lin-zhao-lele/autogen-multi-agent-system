"""
Main entry point for the AutoGen multi-agent code generation web application.
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from config.settings import settings
from web.api import api_router

# Create the FastAPI app
app = FastAPI(
    title="AutoGen Multi-Agent Code Generation System",
    description="A web API for generating, reviewing, and optimizing Python code using AutoGen agents",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)

# Serve static files
static_dir = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# In-memory storage for tasks (in production, use a database)
tasks_storage = {}


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AutoGen Multi-Agent Code Generation System",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "web.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.app_env == "development",
        log_level=settings.log_level.lower()
    )