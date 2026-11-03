import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# 1. DATABASE CONFIGURATION
DATABASE_URL = "postgresql+asyncpg://admin:Ma653390@localhost:5432/northwind"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_kv = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class UserTable(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

# 2. LIFESPAN MANAGEMENT (Creates tables on startup)
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

# 3. FASTAPI INSTANTIATION (Crucial: Must happen BEFORE defining routes!)
app = FastAPI(title="Async FastAPI", lifespan=lifespan)

# 4. SCHEMAS
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# 5. DEPENDENCY
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_kv() as session:
        yield session

# 6. ROUTE ENDPOINTS
@app.get("/tools")
async def get_tools():
    return {"message": "Tools endpoint is working!"}

@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = UserTable(name=user_in.name, email=user_in.email)
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
@app.post("/add", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = UserTable(name=user_in.name, email=user_in.email)
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered")

@app.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await db.get(UserTable, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    return db_user