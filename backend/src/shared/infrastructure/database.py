from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import settings


def _build_async_url(db_url: str) -> tuple[str, dict]:
    """Convert a postgres:// or postgresql:// URL to postgresql+asyncpg://.

    asyncpg does not accept the libpq ``sslmode`` query parameter directly.
    SQLAlchemy translates it, but stripping it from the URL and passing
    ``ssl=True`` via *connect_args* is more reliable across driver versions.

    Returns the cleaned async URL and a ``connect_args`` dict.
    """
    if db_url.startswith("postgresql://"):
        url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif db_url.startswith("postgres://"):
        url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
    else:
        url = db_url

    parsed = urlparse(url)
    params = parse_qs(parsed.query, keep_blank_values=True)

    ssl_mode = params.pop("sslmode", [None])[0]

    new_query = urlencode({k: v for k, v in params.items()}, doseq=True)
    clean_url = urlunparse(parsed._replace(query=new_query))

    connect_args: dict = {}
    if ssl_mode and ssl_mode != "disable":
        connect_args["ssl"] = True

    return clean_url, connect_args


_async_url, _connect_args = _build_async_url(settings.DATABASE_URL)

engine = create_async_engine(
    _async_url,
    echo=settings.is_development,
    connect_args=_connect_args,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
