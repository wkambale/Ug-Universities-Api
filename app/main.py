import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.database import engine, Base
from app.universities.router import router as universities_router
from app.stats.router import router as stats_router
from app.core.health import router as health_router
from app.core.exceptions import global_exception_handler, http_exception_handler
from app.config import settings

logger = logging.getLogger("uvicorn.error")


# ── Security headers middleware ──────────────────────────────────
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Inject security-related HTTP headers on every response."""

    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
        if settings.ENVIRONMENT == "production":
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )
        return response


# ── Lifespan ─────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Auto-create tables in dev/test; use Alembic in production
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


# ── App factory ──────────────────────────────────────────────────
app = FastAPI(
    title="Uganda Universities API",
    version="2.0.0",
    description="A REST API listing universities in Uganda with geo, domain, and type data.",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── Middleware ───────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # public read API — open CORS
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
    expose_headers=["Content-Disposition"],
    max_age=600,
)
app.add_middleware(SecurityHeadersMiddleware)

# ── Exception handlers ──────────────────────────────────────────
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

# ── Routers ─────────────────────────────────────────────────────
app.include_router(
    universities_router, prefix="/api/v1/universities", tags=["Universities"]
)
app.include_router(stats_router, prefix="/api/v1/stats", tags=["Stats"])
app.include_router(health_router, tags=["Health"])


@app.get("/", tags=["Root"])
async def root():
    """API root — returns service metadata and documentation links."""
    return {
        "name": "Uganda Universities API",
        "version": "2.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "universities": "/api/v1/universities/",
        "stats": "/api/v1/stats/",
    }
