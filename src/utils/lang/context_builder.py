# src\utils\lang\context_builder.py
from typing import Dict, Any

def build_context(thread_type: str, item_id: str = None, entity_id: str = None) -> Dict[str, Any]:
    base = {}
    print("")
    
    if thread_type == "company":
        base["sub_module"] = "company_profile"
        base["company_id"] = entity_id
    elif thread_type == "product":
        base["sub_module"] = "product"
        base["item_id"] = entity_id
        base["product_id"] = item_id
    elif thread_type == "service":
        base["sub_module"] = "service"
        base["service_id"] = item_id
    else:
        base["sub_module"] = thread_type  # fallback
    
    return base