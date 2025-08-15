# src\utils\lang\context_builder.py
from typing import Dict, Any


def build_context(thread_type: str, entity_id: str = None) -> Dict[str, Any]:
    base = {}

    if thread_type == "company":
        base["sub_module"] = "company"
        base["company_id"] = entity_id
    elif thread_type == "product":
        base["sub_module"] = "product"
        base["item_id"] = entity_id

    else:
        base["sub_module"] = thread_type  # fallback

    return base
