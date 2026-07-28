from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from api.exceptions import setup_exception_handlers
from api.routes import chat, complaints, upload, health

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    setup_exception_handlers(app)

    app.include_router(health.router, prefix="/health", tags=["Health"])
    app.include_router(chat.router, prefix="/api/chat", tags=["Chat & AI"])
    app.include_router(upload.router, prefix="/api/upload", tags=["Document Upload"])
    app.include_router(complaints.router, prefix="/api/complaints", tags=["Complaints"])

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
