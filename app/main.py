import logging
from contextlib import asynccontextmanager
from core.db import db_helper
import uvicorn
from fastapi import FastAPI
from api import router as api_router
from core.config import settings
from middleware.error_handler import app_exception_handler
from utils.exceptions import AppError


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    yield
    await db_helper.dispose()


logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
)
app = FastAPI(
    lifespan=lifespan,
)

app.add_exception_handler(AppError, app_exception_handler)

app.include_router(
    api_router,
    prefix=settings.api_prefix.prefix,
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=settings.run.reload,
        host=settings.run.host,
        port=settings.run.port,
    )
