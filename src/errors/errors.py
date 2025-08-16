# src\errors\errors.py
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from starlette import status
import traceback
from src.utils.logging import setup_logging
from src.config import settings
from .custom_exceptions import MissingEnvVarError
from .shared import http_error, extract_location, log_error

logger = setup_logging(__name__)


async def integrity_error(request: Request, exc: IntegrityError):
    location = extract_location(exc)
    log_error("IntegrityError", str(exc), location, str(request.url))

    return http_error(
        "Invalid reference or unique constraint failed",
        code="integrity_error",
        status_code=status.HTTP_400_BAD_REQUEST,
        meta={"location": location} if settings.DEBUG else None,
    )


async def validation_error(request: Request, exc: RequestValidationError):
    log_error("ValidationError", str(exc), "validation", str(request.url))

    return http_error(
        "Invalid input",
        code="validation_error",
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        meta={"errors": exc.errors(), "path": str(request.url)},
    )


async def generic_error(request: Request, exc: Exception):
    error_type = exc.__class__.__name__
    location = extract_location(exc)
    log_error(error_type, str(exc), location, str(request.url))

    if settings.DEBUG:
        traceback.print_exc()

    return http_error(
        "Internal error",
        code="internal_error",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        meta={"location": location} if settings.DEBUG else None,
    )


async def missing_env_error(request: Request, exc: MissingEnvVarError):
    log_error("MissingEnvVarError", str(exc), "config", str(request.url))
    return http_error(str(exc), code="missing_env_var", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
