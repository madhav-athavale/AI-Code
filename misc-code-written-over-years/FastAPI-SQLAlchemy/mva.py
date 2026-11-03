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

class STATE(Base):
    __tablename__ = "us_states"

    state_id: Mapped[int] = mapped_column( primary_key=True)
    state_name: Mapped[str] = mapped_column(String(100))
    state_abbr: Mapped[str]  = mapped_column(String(2))
    state_region: Mapped[str]  = mapped_column(String(50))

# 2. LIFESPAN MANAGEMENT (Creates tables on startup)
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

# 3. FASTAPI INSTANTIATION (Crucial: Must happen BEFORE defining routes!)
app = FastAPI(title="Async FastAPI", lifespan=lifespan)

# 4. SCHEMAS
class STATEBase(BaseModel):
    state_id : int
    state_name: str
    state_abbr: str
    state_region: str

class STATECreate(STATEBase):
    pass

class STATEResponse(STATEBase):
    state_id: int
    model_config = ConfigDict(from_attributes=True)

# 5. DEPENDENCY
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_kv() as session:
        yield session

# 6. ROUTE ENDPOINTS
@app.get("/tools")
async def get_tools():
    return {"message": "Tools endpoint is working!"}

@app.post("/states", response_model=STATEResponse, status_code=status.HTTP_201_CREATED)
async def create_state(state_in: STATECreate, db: AsyncSession = Depends(get_db)):
    db_state = STATE(state_id = state_in.state_id,state_name=state_in.state_name, state_abbr=state_in.state_abbr, state_region= state_in.state_region)
    db.add(db_state)
    try:
        await db.commit()
        await db.refresh(db_state)
        return db_state
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")

@app.get("/states/{state_id}", response_model=STATEResponse)
async def read_state(state_id: int, db: AsyncSession = Depends(get_db)):
    db_state = await db.get(STATE, state_id)
    if not db_state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="state not found"
        )
    return db_state