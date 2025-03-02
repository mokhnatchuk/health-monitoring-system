import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Завантаження змінних середовища
load_dotenv()

# Створення базового класу для ORM-моделей
Base = declarative_base()

# Отримання URL бази даних
DATABASE_URL = os.getenv("DATABASE_URL")

# Перевірка наявності змінної DATABASE_URL у середовищі
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Заміна стандартного postgresql:// на postgresql+asyncpg:// для асинхронної роботи
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# Створення асинхронного двигуна для підключення до БД
engine = create_async_engine(DATABASE_URL, echo=True)

# Створення фабрики сесій БД
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Функція для отримувати сесії БД
async def get_db():
    db_session = AsyncSessionLocal()
    try:
        yield db_session
    finally:
        await db_session.close()
