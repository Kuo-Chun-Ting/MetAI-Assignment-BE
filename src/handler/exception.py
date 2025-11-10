from fastapi import Request
from fastapi.responses import JSONResponse

from src.service.error import ServiceError


async def service_error_handler(_: Request, exc: ServiceError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def generic_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    # In a real-world scenario, you would want to log the exception `exc` here
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


def add_exception_handlers(app):
    app.add_exception_handler(ServiceError, service_error_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
