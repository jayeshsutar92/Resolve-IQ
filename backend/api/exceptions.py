from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from utils.logger import get_logger

logger = get_logger(__name__)

def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "An unexpected error occurred.", "details": str(exc)}
        )
