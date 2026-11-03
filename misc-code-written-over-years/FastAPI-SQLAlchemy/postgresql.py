import asyncio
import asyncpg
from dotenv import load_dotenv
import os

load_dotenv()


# def jls_extract_def(conn):
#     # 2. Create a sample table
#     print("Creating table...")
#     await conn.execute('''
#         CREATE TABLE IF NOT EXISTS users (
#             id SERIAL PRIMARY KEY,
#             name TEXT NOT NULL,
#             email TEXT UNIQUE NOT NULL
#         );
#     ''')
    
#     # 3. Insert data using positional parameters ($1, $2)
#     # asyncpg does NOT use %s or %(name)s syntax
#     print("Inserting user data...")
#     await conn.execute('''
#         INSERT INTO users (name, email) 
#         VALUES ($1, $2) 
#         ON CONFLICT (email) DO NOTHING;
#     ''', 'Alice Smith', 'alice@example.com')
    
#     # 4. Bulk insert multiple records efficiently using executemany
#     print("Bulk inserting records...")
#     users_to_add = [
#         ('Bob Jones', 'bob@example.com'),
#         ('Charlie Brown', 'charlie@example.com')
#     ]
#     await conn.executemany('''
#         INSERT INTO users (name, email) 
#         VALUES ($1, $2) 
#         ON CONFLICT (email) DO NOTHING;
#     ''', users_to_add)
    
#     return users_to_add


async def main():
    load_dotenv()
    USER = os.environ.get("USER")
    PASSWORD = os.environ.get("PASSWORD")
    DATABASE = os.environ.get("DATABASE")
    
    print(USER)
    # 1. Establish a connection to the PostgreSQL database
    # (Replace credentials with your local or environment variables)
    # conn = await asyncpg.connect(
    #     user='postgres', 
    #     password='secret_password',
    #     database='my_database', 
    #     host='127.0.0.1',
    #     port=5432
    # )
    
    conn = await asyncpg.connect(
        user=USER, 
        password=PASSWORD,
        database=DATABASE,
        host='127.0.0.1',
        port=5432
    )

    try:
    #    users_to_add = jls_extract_def(conn)
        # 5. Fetch a single row
        print("\n--- Fetching a single row ---")
        row = await conn.fetchrow('SELECT * FROM customers')
        if row:
            # You can access columns by index or by name like a dictionary
            print(f"Contact_name: {row['contact_name']}")

        async with conn.transaction():
           async for record in conn.cursor("SELECT contact_name FROM customers"):
             print(list(record)[0])

 

        # 6. Fetch multiple rows
        # print("\n--- Fetching all rows ---")
        # rows = await conn.fetch('SELECT id, name, email FROM users ORDER BY id ASC')
        # for row in rows:
        #     print(f"[{row['id']}] {row['name']} (<{row['email']}>)")

    finally:
        # 7. Always ensure the connection is closed
        print("\nClosing database connection...")
        await conn.close()

# Run the async loop
if __name__ == "__main__":
    asyncio.run(main())
