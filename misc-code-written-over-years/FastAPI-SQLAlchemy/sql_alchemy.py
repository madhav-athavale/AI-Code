from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session

engine = create_engine("sqlite:///test.db")
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)

# Create tables
Base.metadata.create_all(engine)

# Insert
with Session(engine) as session:
    session.add(User(name="Alice"))
    session.add(User(name="Bob"))
    session.commit()

# Query
with Session(engine) as session:
    users = session.query(User).all()
    for u in users:
        print(u.name)