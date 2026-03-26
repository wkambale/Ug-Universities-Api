from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from enum import Enum
from datetime import datetime

class UniversityType(str, Enum):
    public   = "public"
    private  = "private"
    military = "military"

class UniversityBase(BaseModel):
    name:             str
    abbrev:           Optional[str] = None
    location:         str
    type:             UniversityType
    domains:          List[str] = []
    web_pages:        List[str] = []
    latitude:         Optional[float] = None
    longitude:        Optional[float] = None
    established:      Optional[int] = None
    logo_url:         Optional[str] = None

class UniversityCreate(UniversityBase):
    pass

class UniversityUpdate(BaseModel):
    name:             Optional[str] = None
    abbrev:           Optional[str] = None
    location:         Optional[str] = None
    type:             Optional[UniversityType] = None
    domains:          Optional[List[str]] = None
    web_pages:        Optional[List[str]] = None
    latitude:         Optional[float] = None
    longitude:        Optional[float] = None
    established:      Optional[int] = None
    logo_url:         Optional[str] = None

class UniversityOut(UniversityBase):
    id:               int
    alpha_two_code:   str
    alpha_three_code: str
    country:          str
    is_active:        bool
    created_at:       datetime
    updated_at:       Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class UniversityGeo(BaseModel):
    id:        int
    name:      str
    abbrev:    Optional[str] = None
    location:  str
    type:      UniversityType
    latitude:  Optional[float] = None
    longitude: Optional[float] = None
    
    model_config = ConfigDict(from_attributes=True)
