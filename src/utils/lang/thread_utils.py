# src\utils\lang\thread_utils.py
import hashlib
from typing import Optional
from src.types_.thread_types import Module, ThreadType

def generate_thread_id(
    user_id: str,
    company_id: str,
    module: Module,
    thread_type: ThreadType = ThreadType.MODULE,
    item_id: Optional[str] = None,
) -> str:
    if thread_type == ThreadType.MODULE:
        key = f"{user_id}:{company_id}:{module.value}"
    elif thread_type == ThreadType.COMPANY:
        key = f"{user_id}:{company_id}:{module.value}:company"
    elif thread_type == ThreadType.PRODUCT:
        key = f"{user_id}:{company_id}:{module.value}:product:{item_id}"
    elif thread_type == ThreadType.CHANNEL:
        key = f"{user_id}:{company_id}:{module.value}:channel:{item_id}"
    else:
        raise ValueError("Unsupported thread type")

    return hashlib.md5(key.encode()).hexdigest()
