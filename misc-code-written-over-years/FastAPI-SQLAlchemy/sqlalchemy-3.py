from sqlalchemy import create_engine, text, inspect
from sqlalchemy.engine import URL
import json
import pandas as pd
from sqlalchemy.orm import  Session

connection_url = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password="Pma94029@",  # passed directly, no URL encoding needed
    host="127.0.0.1",
    port=3306,
    database="northwind"
)
engine = create_engine(connection_url, connect_args={"charset": "utf8mb4"})

inspector = inspect(engine)

#print(inspector.get_table_names())

print("****")

#

#df = pd.read_sql("select * from customers", engine)

#print(df.head())

def extract_count():
    with Session(engine) as session:
        result = session.execute(text("select count(*) from customers"))
        print(result.fetchone()[0])
    return result


extract_count()
    


        # Update
with Session(engine) as session:
    try:
        # Insert
        session.execute(text("""
            INSERT INTO strings (string_id, string_data)
            VALUES (:id, :data)"""), {
            "id": 116,
            "data": "Test Company"
            
        })

        # Update
        # session.execute(text("""
        #     UPDATE customers 
        #     SET city = :city 
        #     WHERE customerID = :id
        # """), {
        #     "city": "Miami",
        #     "id": "TESTCO"
        # })

        # Commit both together
        session.commit()
        print("All changes committed!")

    except Exception as e:
        session.rollback()  # undo everything if error
        print(f"Error: {e}")

     