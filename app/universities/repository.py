from typing import List, Optional, Tuple
from sqlalchemy import select, func, or_, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from app.universities.models import University
from app.universities.schemas import UniversityCreate, UniversityUpdate
from app.universities.filters import UniversityFilters

class UniversityRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, filters: UniversityFilters) -> Tuple[List[University], int]:
        query = select(University)
        
        # Apply filters
        if filters.is_active is not None:
            query = query.filter(University.is_active == filters.is_active)
        if filters.type:
            query = query.filter(University.type == filters.type)
        if filters.location:
            query = query.filter(University.location.ilike(f"%{filters.location}%"))
        if filters.search:
            search_pattern = f"%{filters.search}%"
            query = query.filter(
                or_(
                    University.name.ilike(search_pattern),
                    University.abbrev.ilike(search_pattern),
                    University.location.ilike(search_pattern)
                )
            )
            
        # Total count before pagination
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total_count = total_result.scalar() or 0
        
        # Ordering
        if filters.ordering:
            order_field = filters.ordering.lstrip("-")
            if hasattr(University, order_field):
                col = getattr(University, order_field)
                if filters.ordering.startswith("-"):
                    query = query.order_by(desc(col))
                else:
                    query = query.order_by(asc(col))
        else:
            query = query.order_by(asc(University.name))
            
        # Pagination
        query = query.offset((filters.page - 1) * filters.page_size).limit(filters.page_size)
        
        result = await self.db.execute(query)
        return list(result.scalars().all()), total_count

    async def get_by_id(self, university_id: int) -> Optional[University]:
        result = await self.db.execute(select(University).filter(University.id == university_id))
        return result.scalar_one_or_none()

    async def create(self, data: UniversityCreate) -> University:
        university = University(**data.model_dump())
        self.db.add(university)
        await self.db.commit()
        await self.db.refresh(university)
        return university

    async def update(self, university_id: int, data: UniversityUpdate) -> Optional[University]:
        university = await self.get_by_id(university_id)
        if not university:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(university, key, value)
            
        await self.db.commit()
        await self.db.refresh(university)
        return university

    async def delete(self, university_id: int) -> bool:
        university = await self.get_by_id(university_id)
        if not university:
            return False
        
        # Soft delete
        university.is_active = False
        await self.db.commit()
        return True

    async def get_geo(self) -> List[University]:
        # Filter for universities with lat/lng
        result = await self.db.execute(
            select(University).filter(
                University.latitude.isnot(None),
                University.longitude.isnot(None),
                University.is_active == True
            )
        )
        return list(result.scalars().all())

    async def get_domains(self) -> List[str]:
        result = await self.db.execute(select(University.domains).filter(University.is_active == True))
        domains = []
        for row in result.all():
            if row[0]:
                domains.extend(row[0])
        return sorted(list(set(domains)))

    async def get_locations(self) -> List[str]:
        result = await self.db.execute(
            select(University.location)
            .filter(University.is_active == True)
            .distinct()
        )
        return sorted([row[0] for row in result.all()])

    async def get_count_by_type(self) -> dict:
        result = await self.db.execute(
            select(University.type, func.count())
            .filter(University.is_active == True)
            .group_by(University.type)
        )
        return {row[0]: row[1] for row in result.all()}
        
    async def get_all_for_export(self) -> List[University]:
        result = await self.db.execute(select(University).order_by(asc(University.id)))
        return list(result.scalars().all())
