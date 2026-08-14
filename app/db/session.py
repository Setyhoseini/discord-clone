from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# ---- Ensure we use asyncpg driver ----
database_url = settings.DATABASE_URL
if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
elif database_url.startswith("postgresql+asyncpg://"):
    # Already correct – keep as is
    pass
else:
    # If it's something else (e.g., sqlite), you may want to handle it, but we expect postgres
    # We'll still use it as is, but the async engine might fail.
    pass

# 1. ساخت Engine برای اتصال به PostgreSQL
# echo=True باعث می‌شود کوئری‌های SQL در کنسول لاگ شوند (برای دیباگ عالی است)
engine = create_async_engine(
    database_url,   # 👈 use the transformed URL
    echo=True,
    pool_pre_ping=True, # برای جلوگیری از قطعی‌های ناگهانی دیتابیس
)

# 2. تنظیم Session Factory برای ایجاد نشست‌های دیتابیس
AsyncSessionLocal = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# 3. کلاس Base برای مدل‌ها (فعلاً خالی است تا مدل‌ها را بعداً اضافه کنید)
Base = declarative_base()

# 4. تابع کمکی برای دریافت Session در مسیرهای API
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()