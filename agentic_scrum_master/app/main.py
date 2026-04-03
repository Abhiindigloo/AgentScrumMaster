from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.logging_config import setup_logging, get_logger
from app.core.exceptions import AppException

logger = get_logger(__name__)


def create_app() -> FastAPI:
    """Application factory — builds and returns the FastAPI instance."""
    settings = get_settings()
    setup_logging()

    application = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="AI-powered Scrum facilitation agent.",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _register_exception_handlers(application)
    _register_routes(application)

    logger.info(
        "%s v%s initialized (debug=%s)",
        settings.APP_NAME,
        settings.APP_VERSION,
        settings.DEBUG,
    )
    return application


def _register_exception_handlers(application: FastAPI) -> None:
    @application.exception_handler(AppException)
    async def handle_app_exception(
        request: Request, exc: AppException
    ) -> JSONResponse:
        logger.warning("AppException: %s (status=%d)", exc.message, exc.status_code)
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.message,
                "details": exc.details,
            },
        )

    @application.exception_handler(Exception)
    async def handle_unhandled_exception(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.error("Unhandled exception: %s", exc, exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Internal server error",
            },
        )


def _register_routes(application: FastAPI) -> None:
    @application.get("/api/healthz", tags=["health"])
    async def healthz() -> dict:
        settings = get_settings()
        return {
            "status": "ok",
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
        }


app = create_app()
