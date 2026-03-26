from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.database import engine, Base
from app.universities.router import router as universities_router
from app.stats.router import router as stats_router
from app.core.health import router as health_router
from app.core.exceptions import global_exception_handler, http_exception_handler
from fastapi.exceptions import HTTPException

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This automatically creates tables in local dev/testing
    # In production, recommend using Alembic migrations
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(
    title="Uganda Universities API",
    version="2.0.0",
    description="A REST API listing universities in Uganda with geo, domain, and type data.",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Exception Handlers
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

# Routers
app.include_router(universities_router, prefix="/api/v1/universities", tags=["Universities"])
app.include_router(stats_router, prefix="/api/v1/stats", tags=["Stats"])
app.include_router(health_router, tags=["Health"])

@app.get("/", tags=["Root"])
async def root():
    return {
        "name": "Uganda Universities API",
        "version": "2.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "universities": "/api/v1/universities/",
        "stats": "/api/v1/stats/",
    }
