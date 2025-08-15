# src\types_\thread_types.py
from typing import Optional
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
    ONBOARDING = "onboarding"
    ONBOARDED = "onboarded"
    COMPANY_PROFILE_COMPLETED = "company_profile_completed"
    PRODUCTS_ADDED = "products_added"
    CHANNELS_INTEGRATED = "channels_integrated"
    HOME_COMPLETED = "home_completed"


@dataclass
class ThreadInfo:
    thread_id: str
    
    parent_thread_id: Optional[str]
    
    