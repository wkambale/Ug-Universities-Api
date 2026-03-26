import json
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy import ARRAY as PG_ARRAY
from sqlalchemy.sql import func
from sqlalchemy.types import TypeDecorator
from app.database import Base

class StringArray(TypeDecorator):
    """
    A portable list-of-strings column.
    • PostgreSQL  → uses native ARRAY(String) for indexing / unnest support.
    • SQLite/other → stores JSON-encoded text (used in test suite).
    """
    impl = Text
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(PG_ARRAY(String))
        return dialect.type_descriptor(Text())

    def process_bind_param(self, value, dialect):
        if dialect.name == "postgresql":
            return value
        return json.dumps(value or [])

    def process_result_value(self, value, dialect):
        if dialect.name == "postgresql":
            return value or []
        if isinstance(value, str):
            return json.loads(value)
        return value or []

class University(Base):
    __tablename__ = "universities"

    id               = Column(Integer, primary_key=True, index=True)
    name             = Column(String(255), unique=True, nullable=False, index=True)
    abbrev           = Column(String(20), nullable=True)
    location         = Column(String(100), nullable=False, index=True)
    type             = Column(String(20), nullable=False, index=True)  # public | private | military
    domains          = Column(StringArray, default=[])
    web_pages        = Column(StringArray, default=[])
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
