from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

pas = "test@123"
DB_CONFIG = f"postgresql+asyncpg://test:{pas}@localhost:5432/test1"

SECRET_KEY = "test@123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AsyncDatabaseSession:

    def __init__(self) -> None:
        self.session = None
        self.engine = None

    def __getattr__(self,name):
        return getattr(self.session,name)

    def init(self):
        self.engine = create_async_engine(DB_CONFIG,future=True, echo=True)
        self.session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)()

    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

# db is an instance of AsyncDatabaseSession.
db = AsyncDatabaseSession()

"""
    commit_rollback is an asynchronous function:
        ? Attempts to commit the database session.
        ? If an exception occurs, rolls back the session and re-raises the exception.
"""
async def commit_rollback():
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise