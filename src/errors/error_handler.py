# src\errors\error_handler.py
from fastapi import Request
from fastapi.responses import JSONResponse
import traceback
import logging
import os

# Set up clean logging
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


async def global_exception_handler(request: Request, exc: Exception):
    error_type = exc.__class__.__name__
    error_msg = str(exc)

    try:
        tb = traceback.extract_tb(exc.__traceback__)
        file_name = tb[-1].filename.split("/")[-1]
        line_num = tb[-1].lineno
    except Exception:
        file_name = "unknown"
        line_num = "?"

    logger.error(f"{error_type}: {error_msg} | {file_name}:{line_num}")

    debug_mode = os.getenv("DEBUG", "false").lower() == "true"
    if debug_mode:
        traceback.print_exc()

    return JSONResponse(
        status_code=getattr(exc, "status_code", 500),
        content={
            "error": error_type,
            "message": error_msg if debug_mode else "Internal server error",
            "location": f"{file_name}:{line_num}",
            "path": str(request.url),
        },
    )
