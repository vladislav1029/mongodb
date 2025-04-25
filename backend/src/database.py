from typing import Annotated, AsyncGenerator
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


async def get_database() -> AsyncGenerator[AsyncIOMotorDatabase, None]:
    client: AsyncIOMotorClient = AsyncIOMotorClient(settings.MONGO_URI)
    db: AsyncIOMotorDatabase = client[settings.MONGO_NAME]  # Имя базы данных
    try:
        yield db
    finally:
        client.close()


AsyncDep = Annotated[AsyncIOMotorDatabase, Depends(get_database)]
