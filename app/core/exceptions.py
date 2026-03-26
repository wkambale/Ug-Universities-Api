from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.responses import error_response

async def global_exception_handler(request: Request, exc: Exception):
    return error_response(
        message=f"An unexpected error occurred: {str(exc)}",
        code=500
    )

async def http_exception_handler(request: Request, exc: Exception):
    # This handles both standard HTTPException and custom ones
    status_code = getattr(exc, "status_code", 400)
    detail = getattr(exc, "detail", "Unknown error")
    return error_response(
        message=detail,
        code=status_code
    )
