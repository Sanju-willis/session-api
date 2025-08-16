# src\errors\error_handler.py
from fastapi import Request
from src.errors.shared import http_error, extract_location, log_error
from src.config import settings


async def global_exception_handler(request: Request, exc: Exception):
    error_type = exc.__class__.__name__
    error_msg = str(exc)
    location = extract_location(exc)

    log_error(error_type, error_msg, location, str(request.url))

    if settings.DEBUG:
        import traceback

        traceback.print_exc()

    return http_error(
        message=error_msg if settings.DEBUG else "Internal server error",
        code=error_type,
        status_code=getattr(exc, "status_code", 500),
        meta={"location": location, "path": str(request.url)},
    )
