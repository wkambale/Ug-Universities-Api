from typing import Optional
from pydantic import BaseModel, Field
from app.universities.schemas import UniversityType

class UniversityFilters(BaseModel):
    type:      Optional[UniversityType] = None
    location:  Optional[str] = None
    search:    Optional[str] = None
    is_active: Optional[bool] = True
    ordering:  Optional[str] = None
    page:      int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
