from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

connection_url = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password="Pma94029@",  # passed directly, no URL encoding needed
    host="127.0.0.1",
    port=3306,
    database="northwind"
)
engine = create_engine(connection_url, connect_args={"charset": "utf8mb4"})

with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM Strings"))
    for row in result:
        print(row)