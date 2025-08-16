# src\errors\shared.py
from fastapi.responses import JSONResponse
import traceback
from src.utils import setup_logging

logger = setup_logging(__name__)

def http_error(message, code="bad_request", status_code=400, meta=None):
    return JSONResponse(
        {"error": {"code": code, "message": message, "meta": meta or {}}},
        status_code=status_code,
    )

def extract_location(exc: Exception) -> str:
    try:
        tb = traceback.extract_tb(exc.__traceback__)
        file_name = tb[-1].filename.split("/")[-1]
        line_num = tb[-1].lineno
        return f"{file_name}:{line_num}"
    except Exception:
        return "unknown"

def log_error(error_type: str, error_msg: str, location: str, url: str):
    logger.error(f"{error_type}: {error_msg} | {location} | Path: {url}")
