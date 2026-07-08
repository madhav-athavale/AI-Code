import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

conn = mysql.connector.connect(
    host = os.getenv("DB_HPOST"),
    user = os.getenv("DB_USER"),
    password= os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

sql = "Select * from customers"
cursor = conn.cursor()
cursor.execute(sql)
rows = cursor.fetchall()
for row in rows:
    print(row)
print("Data obtained")
cursor.close()
conn.close()