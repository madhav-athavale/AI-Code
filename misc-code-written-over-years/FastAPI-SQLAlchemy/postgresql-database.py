import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker, declarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
#from .database import Base
from sqlalchemy.orm import declarative_base, sessionmaker


load_dotenv()

# Format: postgresql://user:password@host:port/dbname
#DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/my_db")
DATABASE_URL = os.getenv("DATABASE_URL")
# Create the engine
engine = create_engine(DATABASE_URL)
print(DATABASE_URL)
# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modern SQLAlchemy 2.0 Base Class

class us_states(Base):
    __tablename__ = "us_states"

    state_id = mapped_column(Integer, primary_key=True, index=True)
    state_name = mapped_column(String(100), nullable=False)
    state_abbr = mapped_column(String(2),nullable=False)
    state_region = mapped_column(String(50), nullable= False)

# Dependency to yield a database session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Ensures connections are returned to the pool



    state_id = mapped_column(Integer, primary_key=True, index=True)
    state_name = mapped_column(String(100), nullable=False)
    state_abbr = mapped_column(String(2),nullable=False)
    state_region = mapped_column(String(50), nullable= False)


class UserTable(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
