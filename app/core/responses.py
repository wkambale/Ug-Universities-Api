from typing import Any, Optional
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def success_response(data: Optional[Any] = None, message: str = "success", status_code: int = 200, **kwargs):
    content = {
        "status": "success",
    }
    if data is not None:
        content["data"] = data
    if message != "success":
        content["message"] = message
    
    # Merge additional kwargs (for pagination)
    content.update(kwargs)
    
    return JSONResponse(content=jsonable_encoder(content), status_code=status_code)

def error_response(message: str, code: int = 400):
    return JSONResponse(
        content={
            "status": "error",
            "code": code,
            "message": message
        },
        status_code=code
    )
