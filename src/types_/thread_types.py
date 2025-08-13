# src\types_\thread_types.py
from typing import Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass


class Module(Enum):
    HOME = "home"
    SOCIAL = "social"
    ANALYTICS = "analytics"

class ThreadType(Enum):
    MODULE = "module"
    COMPANY = "company"
    PRODUCT = "product"
    CHANNEL = "channel"

class MessageType(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class HomeStage(Enum):
    ONBOARDED = "onboarded"
    COMPANY_PROFILE_COMPLETED = "company_profile_completed"
    PRODUCTS_ADDED = "products_added"
    CHANNELS_INTEGRATED = "channels_integrated"
    HOME_COMPLETED = "home_completed"


@dataclass
class ThreadInfo:
    thread_id: str
    thread_type: ThreadType
    module: Module
    parent_thread_id: Optional[str]
    item_id: Optional[str]  # For products: product_id, for channels: channel_id
    stage: str
    metadata: Dict[str, Any]
