from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from core.config import get_settings
from core.logging import setup_logging, get_logger
from core.exceptions import AppException
from api.routes.health import router as health_router
from api.routes.standup import router as standup_router

logger = get_logger(__name__)


def create_app() -> FastAPI:
    """Application factory for the FastAPI app."""
    settings = get_settings()
    setup_logging()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="AI-powered Scrum facilitation agent with blocker detection and daily summaries.",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        logger.warning(f"AppException: {exc.message} (status={exc.status_code})")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.message,
                "details": exc.details,
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Internal server error",
            },
        )

    app.include_router(health_router, prefix="/api")
    app.include_router(standup_router, prefix="/api")

    logger.info(f"{settings.APP_NAME} v{settings.APP_VERSION} initialized")
    return app
