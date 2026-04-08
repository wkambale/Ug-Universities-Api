from typing import List, Optional
import csv
import io
import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.universities.repository import UniversityRepository
from app.universities.schemas import (
    UniversityOut, UniversityGeo, UniversityCreate, UniversityUpdate, UniversityType
)
from app.universities.filters import UniversityFilters
from app.core.responses import success_response, error_response
from app.dependencies import require_admin

logger = logging.getLogger("uvicorn.error")

router = APIRouter()

@router.get("/", response_model=None, summary="List universities", tags=["Universities"])
async def list_universities(
    filters: UniversityFilters = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """List all universities with pagination and filtering."""
    repo = UniversityRepository(db)
    universities, total_count = await repo.get_all(filters)
    
    # Calculate pagination info
    total_pages = (total_count + filters.page_size - 1) // filters.page_size
    next_page = filters.page + 1 if filters.page < total_pages else None
    prev_page = filters.page - 1 if filters.page > 1 else None
    
    # Simple URL generation for pagination
    def get_url(page: Optional[int]):
        if page is None: return None
        return f"/api/v1/universities/?page={page}&page_size={filters.page_size}"

    return {
        "status": "success",
        "count": total_count,
        "page": filters.page,
        "page_size": filters.page_size,
        "total_pages": total_pages,
        "next": get_url(next_page),
        "previous": get_url(prev_page),
        "results": [UniversityOut.model_validate(u) for u in universities]
    }

@router.get("/geo", response_model=None, summary="Universities for Map", tags=["Universities"])
async def geo_universities(db: AsyncSession = Depends(get_db)):
    """Return all active universities with latitude and longitude for map rendering."""
    repo = UniversityRepository(db)
    universities = await repo.get_geo()
    return success_response([UniversityGeo.model_validate(u) for u in universities])

@router.get("/domains", response_model=None, summary="All domains", tags=["Universities"])
async def list_domains(db: AsyncSession = Depends(get_db)):
    """Distinct list of all university domains."""
    repo = UniversityRepository(db)
    domains = await repo.get_domains()
    return success_response(domains)

@router.get("/locations", response_model=None, summary="Distinct locations", tags=["Universities"])
async def list_locations(db: AsyncSession = Depends(get_db)):
    """Distinct list of all university locations."""
    repo = UniversityRepository(db)
    locations = await repo.get_locations()
    return success_response(locations)

@router.get("/types", summary="Valid types", tags=["Universities"])
async def list_types():
    """Enum of valid university type values."""
    return success_response([t.value for t in UniversityType])

@router.get("/count", summary="Count by type", tags=["Universities"])
async def count_universities(db: AsyncSession = Depends(get_db)):
    """Returns total counts of active universities broken down by type."""
    repo = UniversityRepository(db)
    counts = await repo.get_count_by_type()
    return success_response(counts)

@router.get("/export/json", summary="Export all as JSON", tags=["Universities"])
async def export_json(db: AsyncSession = Depends(get_db)):
    """Download the full dataset as a JSON file."""
    repo = UniversityRepository(db)
    universities = await repo.get_all_for_export()
    results = [UniversityOut.model_validate(u).model_dump(mode="json") for u in universities]
    return success_response(results)

@router.get("/export/csv", summary="Export all as CSV", tags=["Universities"])
async def export_csv(db: AsyncSession = Depends(get_db)):
    """Download the full dataset as a CSV file."""
    repo = UniversityRepository(db)
    universities = await repo.get_all_for_export()
    
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=[
        "id", "name", "abbrev", "location", "type", "domains", "web_pages", 
        "latitude", "longitude", "established", "logo_url", 
        "alpha_two_code", "alpha_three_code", "country", "is_active", 
        "created_at", "updated_at"
    ])
    writer.writeheader()
    for u in universities:
        data = UniversityOut.model_validate(u).model_dump(mode="json")
        # Flatten list fields for CSV (semicolon separated)
        data["domains"] = ";".join(data["domains"])
        data["web_pages"] = ";".join(data["web_pages"])
        writer.writerow(data)
        
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=uganda_universities.csv"}
    )

@router.get("/{id}", response_model=None, summary="Retrieve university", tags=["Universities"])
async def get_university(id: int, db: AsyncSession = Depends(get_db)):
    """Single university by ID."""
    repo = UniversityRepository(db)
    university = await repo.get_by_id(id)
    if not university:
        return error_response(message="University not found", code=status.HTTP_404_NOT_FOUND)
    return success_response(UniversityOut.model_validate(university))

# --- Write Endpoints (Admin Required) ---

@router.post("/", dependencies=[Depends(require_admin)], response_model=None, status_code=status.HTTP_201_CREATED, summary="Create university", tags=["Universities"])
async def create_university(data: UniversityCreate, db: AsyncSession = Depends(get_db)):
    """Create a new university record. Requires admin bearer token."""
    repo = UniversityRepository(db)
    try:
        university = await repo.create(data)
        return success_response(UniversityOut.model_validate(university), status_code=status.HTTP_201_CREATED)
    except Exception as e:
        logger.exception("Failed to create university: %s", data.name)
        return error_response(message="Could not create university. It may already exist.", code=400)

@router.put("/{id}", dependencies=[Depends(require_admin)], response_model=None, summary="Full update university", tags=["Universities"])
async def update_university_full(id: int, data: UniversityUpdate, db: AsyncSession = Depends(get_db)):
    """Full update of an existing university. Requires admin bearer token."""
    repo = UniversityRepository(db)
    university = await repo.update(id, data)
    if not university:
        return error_response(message="University not found", code=status.HTTP_404_NOT_FOUND)
    return success_response(UniversityOut.model_validate(university))

@router.patch("/{id}", dependencies=[Depends(require_admin)], response_model=None, summary="Partial update university", tags=["Universities"])
async def update_university_partial(id: int, data: UniversityUpdate, db: AsyncSession = Depends(get_db)):
    """Partial update of an existing university. Requires admin bearer token."""
    repo = UniversityRepository(db)
    university = await repo.update(id, data)
    if not university:
        return error_response(message="University not found", code=status.HTTP_404_NOT_FOUND)
    return success_response(UniversityOut.model_validate(university))

@router.delete("/{id}", dependencies=[Depends(require_admin)], summary="Soft-delete university", tags=["Universities"])
async def delete_university(id: int, db: AsyncSession = Depends(get_db)):
    """Soft-delete a university by setting its `is_active` flag to False. Requires admin bearer token."""
    repo = UniversityRepository(db)
    success = await repo.delete(id)
    if not success:
        return error_response(message="University not found", code=status.HTTP_404_NOT_FOUND)
    return success_response(message="University soft-deleted successfully")
