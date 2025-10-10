from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException
from utils.exceptions import (
    AppError,
    NotFoundError,
    AlreadyExistsError,
)


async def app_exception_handler(request: Request, exc: AppError):
    if isinstance(exc, NotFoundError):
        status_code = 404
    elif isinstance(exc, AlreadyExistsError):
        status_code = 409
    else:
        status_code = 400

    return JSONResponse(status_code=status_code, content={"detail": exc.detail})
