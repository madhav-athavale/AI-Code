from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

@app.post("/items/")
async def create_item(item: Item):
    # 'item' is automatically validated as an Item instance.
    # If the client sends 'price': "twenty", FastAPI returns a 422 error automatically.
    return {"item_name": item.name, "total": item.price * 1.1}


###################
from fastapi import Depends, Header, HTTPException

async def verify_token(x_token: str = Header(...)):
    if x_token != "secret-token":
        raise HTTPException(status_code=400, detail="Invalid Token")

@app.get("/protected-route")
async def get_protected_data(auth: None = Depends(verify_token)):
    return {"data": "Secret information"}

#######

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# connect_args is only needed for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# Dependency to get DB session per request
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db  # Provide session to route handler
    finally:
        db.close()  # Guaranteed cleanup after response is sent
        
        
#################

from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

# --- SQLAlchemy Model ---
class ItemModel(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(index=True)
    description: Mapped[str | None] = mapped_column(default=None)

# --- Pydantic Schemas ---
class ItemCreate(BaseModel):
    title: str
    description: str | None = None

class ItemResponse(ItemCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
    
    
##################

from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from database import Base, engine, get_db
import models
import schemas

# Create tables on startup (use Alembic for production migrations)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Type alias for cleaner route signatures
DbSession = Annotated[Session, Depends(get_db)]


@app.post("/items/", response_model=schemas.ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: schemas.ItemCreate, db: DbSession):
    db_item = models.ItemModel(title=item.title, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/items/{item_id}", response_model=schemas.ItemResponse)
def read_item(item_id: int, db: DbSession):
    db_item = db.query(models.ItemModel).filter(models.ItemModel.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


#########

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./app.db"

engine = create_async_engine(ASYNC_DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session