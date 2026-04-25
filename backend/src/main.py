import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.shared.infrastructure.database import Base, engine
from src.domains.auth.presentation.routes import router as auth_router
from src.domains.owner.presentation.routes import router as owner_router
from src.domains.vehicle.presentation.routes import router as vehicle_router
from src.domains.renter.presentation.routes import router as renter_router
from src.domains.rental.presentation.routes import router as rental_router
from src.domains.finance.presentation.routes import router as finance_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created / verified.")
    except Exception as exc:
        logger.error(
            "Could not initialize database on startup: %s. "
            "Check DATABASE_URL and ensure the database is reachable.",
            exc,
        )
    yield


app = FastAPI(
    title="Renovação Locação API",
    description="Marketplace de aluguel de veículos para motoristas de aplicativos – DDD backend",
    version="1.0.0",
    lifespan=lifespan,
)

origins = (
    ["*"]
    if settings.is_development
    else [
        "https://renovacaolocacao.com.br",
        "https://www.renovacaolocacao.com.br",
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(owner_router, prefix="/api/v1")
app.include_router(vehicle_router, prefix="/api/v1")
app.include_router(renter_router, prefix="/api/v1")
app.include_router(rental_router, prefix="/api/v1")
app.include_router(finance_router, prefix="/api/v1")


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok", "environment": settings.ENVIRONMENT}
