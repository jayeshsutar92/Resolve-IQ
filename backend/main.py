"""
main.py
FastAPI application entry point.
Assembles routers, exception handlers, and configures the app.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from api.exceptions import setup_exception_handlers
from api.routes import chat, complaints, upload, health

def create_app() -> FastAPI:
    """
    Creates and configures the FastAPI application instance.
    """
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug
    )

    # CORS Middleware (configurable in production)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Global exception handlers
    setup_exception_handlers(app)

    # Register Routers
    app.include_router(health.router, prefix="/health", tags=["Health"])
    app.include_router(chat.router, prefix="/api/chat", tags=["Chat & AI"])
    app.include_router(upload.router, prefix="/api/upload", tags=["Document Upload"])
    app.include_router(complaints.router, prefix="/api/complaints", tags=["Complaints"])

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
