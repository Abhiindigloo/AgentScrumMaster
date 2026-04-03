import uvicorn

from core.config import get_settings


def main() -> None:
    """Entry point for running the application."""
    settings = get_settings()
    uvicorn.run(
        "api.app:create_app",
        factory=True,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )


if __name__ == "__main__":
    main()
