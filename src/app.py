# src\app.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from .errors import global_exception_handler
from .core.db import Base, engine
from src.routers import session_route, chat_route


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Session API", version="1.0.0", lifespan=lifespan)

    app.add_exception_handler(Exception, global_exception_handler)

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(session_route)
    app.include_router(chat_route)

    # Health
    @app.get("/")
    def root():
        return {"ok": True}

    return app
