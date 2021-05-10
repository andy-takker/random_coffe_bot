import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import SQLALCHEMY_DATABASE_URI
from . import models

engine = create_async_engine(SQLALCHEMY_DATABASE_URI, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def create_db():
    async with engine.begin() as connection:
        await connection.run_sync(models.Base.metadata.create_all)
