from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Define connection string (PostgreSQL uses the psycopg driver)
# Format: postgresql+psycopg://user:password@host:port/dbname
#DATABASE_URL = "postgresql+psycopg://my_project_user:my_secure_password@localhost:5432/my_project_db"
DATABASE_URL = "postgresql+psycopg://admin:Ma653390@localhost:5432/northwind"

# 2. Initialize the Engine and Session Creator
engine = create_engine(DATABASE_URL, echo=True)  # echo=True prints generated SQL to console
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 3. Define your Table Model (maps to 'us_states')
class us_states(Base):
    __tablename__ = "us_states"

    state_id = Column(Integer, primary_key=True, index=True)
    state_name = Column(String(100), nullable=False)
    state_abbr = Column(String(2),nullable=False)
    state_region = Column(String(50), nullable= False)

# 4. Execute Operations inside a Session
def run_app():
    # Base.metadata.create_all(bind=engine) # Uncomment this if you want SQLAlchemy to create tables for you
    
    session = SessionLocal()
    try:
        
        # Create (Insert)
        # new_user = User(name="Bob Coder")
        # session.add(new_user)
        # session.commit()
        # print(f" Successfully inserted user with ID: {new_user.id}")


        # Read (Select All)
        states = session.query(us_states).all()
        print("\n--- us_states in Database ---")
        for state in states:
            print(f"State Name : {state.state_name} | Abbr: {state.state_abbr}")

        # Update
        # user_to_update = session.query(User).filter(User.name == "Bob Coder").first()
        # if user_to_update:
        #     user_to_update.name = "Bob Developer"
        #     session.commit()
        #     print("\n Updated user name.")

    except Exception as e:
        session.rollback()
        print(f"❌ Error occurred: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    run_app()
