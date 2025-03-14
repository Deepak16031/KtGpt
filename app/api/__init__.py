# API module init file
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.router import router
from config import CORS_ORIGINS

def create_app():
    """Create and configure the FastAPI application."""
    app = FastAPI(title="KtGpt API", 
                 description="API for managing programming problems with semantic search",
                 version="1.0.0")
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(router)
    
    return app