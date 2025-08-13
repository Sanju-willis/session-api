# src\errors\error_handler.py
from fastapi import Request
from fastapi.responses import JSONResponse
import traceback
import logging
import os

# Set up clean logging
logging.basicConfig(
    level=logging.ERROR, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def global_exception_handler(request: Request, exc: Exception):
    """Clean global error handler for FastAPI"""
    
    # Get clean error info
    error_type = exc.__class__.__name__
    error_msg = str(exc)
    
    # Get just the relevant traceback line
    tb = traceback.extract_tb(exc.__traceback__)
    file_name = tb[-1].filename.split('/')[-1]
    line_num = tb[-1].lineno
    
    # Log clean version
    logger.error(f"{error_type}: {error_msg} | {file_name}:{line_num}")
    
    # Show full traceback in development only
    if os.getenv("DEBUG", "false").lower() == "true":
        traceback.print_exc()
    
    # Return clean API response
    return JSONResponse(
        status_code=500,
        content={
            "error": error_type,
            "message": error_msg,
            "location": f"{file_name}:{line_num}",
            "path": str(request.url)
        }
    )