import logging

from fastapi import Request
from fastapi.exceptions import HTTPException
from app.core.responses import error_response

logger = logging.getLogger("uvicorn.error")


async def global_exception_handler(request: Request, exc: Exception):
    """
    Catch-all for unhandled exceptions.
    Logs the full traceback server-side but returns a generic
    message to the client — never expose internal details.
    """
    logger.exception("Unhandled exception on %s %s", request.method, request.url.path)
    return error_response(
        message="An internal server error occurred.",
        code=500,
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Custom handler so all HTTPException responses use the standard
    JSON envelope instead of FastAPI's default format.
    """
    status_code = getattr(exc, "status_code", 400)
    detail = getattr(exc, "detail", "Unknown error")
    return error_response(
        message=detail,
        code=status_code,
    )
