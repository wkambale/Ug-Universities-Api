from sqlalchemy import Column, Integer, String, Float, Boolean, ARRAY, DateTime
from sqlalchemy.sql import func
from app.database import Base

class University(Base):
    __tablename__ = "universities"

    id               = Column(Integer, primary_key=True, index=True)
    name             = Column(String(255), unique=True, nullable=False, index=True)
    abbrev           = Column(String(20), nullable=True)
    location         = Column(String(100), nullable=False, index=True)
    type             = Column(String(20), nullable=False, index=True)  # public | private | military
    domains          = Column(ARRAY(String), default=[])
    web_pages        = Column(ARRAY(String), default=[])
    latitude         = Column(Float, nullable=True)
    longitude        = Column(Float, nullable=True)
    established      = Column(Integer, nullable=True)
    logo_url         = Column(String(500), nullable=True)
    alpha_two_code   = Column(String(2), default="UG")
    alpha_three_code = Column(String(3), default="UGA")
    country          = Column(String(100), default="Uganda")
    is_active        = Column(Boolean, default=True, index=True)
    created_at       = Column(DateTime(timezone=True), server_default=func.now())
    updated_at       = Column(DateTime(timezone=True), onupdate=func.now())
