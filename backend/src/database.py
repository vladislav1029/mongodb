from typing import AsyncGenerator
from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings


async def get_database() -> AsyncGenerator:
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.MONGO_NAME]  # Имя базы данных
    try:
        yield db
    finally:
        client.close()
