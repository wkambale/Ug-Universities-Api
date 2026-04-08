from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.universities.models import University
from app.core.responses import success_response

router = APIRouter()

@router.get("/", response_model=None, summary="Overall Statistics", tags=["Stats"])
async def get_stats(db: AsyncSession = Depends(get_db)):
    """Returns overall statistics including totals and breakdowns by location and type."""
    # Total and Active
    total_q = select(func.count(University.id))
    active_q = select(func.count(University.id)).filter(University.is_active.is_(True))
    
    total_res = await db.execute(total_q)
    active_res = await db.execute(active_q)
    
    total = total_res.scalar() or 0
    active = active_res.scalar() or 0
    
    # By Type
    type_q = select(University.type, func.count()).filter(University.is_active.is_(True)).group_by(University.type)
    type_res = await db.execute(type_q)
    by_type = {row[0]: row[1] for row in type_res.all()}
    
    # By Location
    loc_q = select(University.location, func.count()).filter(University.is_active.is_(True)).group_by(University.location).order_by(func.count().desc()).limit(10)
    loc_res = await db.execute(loc_q)
    by_location = {row[0]: row[1] for row in loc_res.all()}
    
    return success_response({
        "total": total,
        "active": active,
        "by_type": by_type,
        "by_location": by_location
    })
