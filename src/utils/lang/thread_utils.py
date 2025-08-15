# src\utils\lang\thread_utils.py
import hashlib
from typing import Optional
from src.types_.thread_types import Module, ThreadType


def generate_thread_id(
    user_id: str,company_id: str,module: Module,thread_type: ThreadType = ThreadType.MODULE,item_id: Optional[str] = None,entity_id: Optional[str] = None,
) -> str:
    key_parts = [user_id, company_id, module.value]

    if thread_type != ThreadType.MODULE:
        key_parts.append(thread_type.value)

    if item_id:
        key_parts.append(item_id)

    if entity_id:
        key_parts.append(entity_id)

    key = ":".join(key_parts)
    return hashlib.md5(key.encode()).hexdigest()
