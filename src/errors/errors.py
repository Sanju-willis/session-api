# src\errors\errors.py
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from starlette import status
import traceback
from src.utils.logging import setup_logging
from ..core.config import settings
from .custom_exceptions import MissingEnvVarError

logger = setup_logging(__name__)

def http_error(message, code="bad_request", status_code=400, meta=None):
   return JSONResponse(
       {"error": {"code": code, "message": message, "meta": meta or {}}},
       status_code=status_code
   )

async def handle_integrity_error(request: Request, exc: IntegrityError):
   # Get error details for logging
   try:
       tb = traceback.extract_tb(exc.__traceback__)
       file_name = tb[-1].filename.split("/")[-1]
       line_num = tb[-1].lineno
       location = f"{file_name}:{line_num}"
   except Exception:
       location = "unknown"
   
   # Log the integrity error
   logger.error(f"IntegrityError: {str(exc)} | {location} | Path: {request.url}")
   
   return http_error(
       "Invalid reference or unique constraint failed",
       code="integrity_error",
       status_code=status.HTTP_400_BAD_REQUEST,
       meta={"location": location} if settings.DEBUG else None
   )

async def handle_validation_error(request: Request, exc: RequestValidationError):
   # Log the validation error
   logger.error(f"ValidationError: {str(exc)} | Path: {request.url}")
   
   return http_error(
       "Invalid input",
       code="validation_error",
       status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
       meta={
           "errors": exc.errors(),
           "path": str(request.url)
       }
   )

async def handle_generic_error(request: Request, exc: Exception):
   # Get error details for logging
   error_type = exc.__class__.__name__
   error_msg = str(exc)
   
   try:
       tb = traceback.extract_tb(exc.__traceback__)
       file_name = tb[-1].filename.split("/")[-1]
       line_num = tb[-1].lineno
       location = f"{file_name}:{line_num}"
   except Exception:
       location = "unknown"
   
   # Log the error
   logger.error(f"{error_type}: {error_msg} | {location} | Path: {request.url}")
   
   # Show full traceback in development
   if settings.DEBUG:
       traceback.print_exc()
   
   return http_error(
       "Internal error",
       code="internal_error",
       status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
       meta={"location": location} if settings.DEBUG else None
   )

async def handle_missing_env_error(request: Request, exc: MissingEnvVarError):
    logger.error(f"MissingEnvVarError: {str(exc)} | Path: {request.url}")
    return http_error(
        str(exc),
        code="missing_env_var",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )