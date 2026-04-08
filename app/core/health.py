from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import get_db
from app.core.responses import error_response

router = APIRouter()

@router.get("/health", tags=["Health"])
async def health():
    """Liveness check - always 200 if container is up."""
    return {"status": "ok"}

@router.get("/ready", tags=["Health"])
async def readiness(db: AsyncSession = Depends(get_db)):
    """Readiness check - verifies DB connectivity."""
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception as e:
        return error_response(message=f"Database connection failed: {str(e)}", code=status.HTTP_503_SERVICE_UNAVAILABLE)
