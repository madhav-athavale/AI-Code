import psycopg

# 1. Define your connection parameters
db_config = {
    "dbname": "northwind",
    "user": "admin",
    "password": "Ma653390@",
    "host": "localhost",
    "port": "5432"
}

try:
    # 2. Establish the connection using a context manager
    with psycopg.connect(**db_config) as conn:
        print(" Successfully connected to PostgreSQL!")
        
        # 3. Create a cursor to execute SQL commands
        with conn.cursor() as cur:
            
            # Example A: Insert data safely using placeholders
            cur.execute(
                "select * from customers;" 
                
            )
            
            # Example B: Fetch and display data
            
            rows = cur.fetchall()
            
            print("\n--- Table Data ---")
            for row in rows:
                print(f"ID: {row[0]} | Name: {row[1]} | contact name: {row[2]}")
                
        # Changes are automatically committed when exiting the block
        print("\n Connection closed safely.")

except Exception as error:
    print(f"❌ Connection failed: {error}")
