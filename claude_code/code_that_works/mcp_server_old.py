"""
MCP Server - Agentic AI Template (MCPServer + Streamable HTTP) — mcp SDK v2
Runs as a standalone HTTP server supporting multiple clients.
Tools: add, subtract, price (Alpha Vantage), query_db (MySQL), write_csv

Install dependencies:
    pip install "mcp>=2,<3" httpx aiomysql python-dotenv

Run:
    python mcp_server.py
Clients connect to:
    http://localhost:8000/mcp
"""

import os
import csv
import httpx
import aiomysql
from dotenv import load_dotenv
from mcp.server.mcpserver import MCPServer
import asyncpg

load_dotenv()

# v2: host/port are no longer constructor args — they move to run()
mcp = MCPServer("calculator-server")

AV_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "db": os.getenv("DB_NAME"),
}

POSTGRESQL_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    # "port": int(os.getenv("POS_PORT")),
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
    "database": os.getenv("DATABASE"),
}

 
# ── Tools ────────────────────────────────────────────────────────────────────

@mcp.tool()
def add(a: float, b: float) -> str:
    """Adds two numbers together."""
    return f"{a} + {b} = {a + b}"


@mcp.tool()
def subtract(a: float, b: float) -> str:
    """Subtracts the second number from the first."""
    return f"{a} - {b} = {a - b}"


@mcp.tool()
async def price(symbol: str) -> str:
    """Find the current stock price for a ticker symbol, e.g. MSFT, AAPL."""
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": AV_API_KEY,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get("https://www.alphavantage.co/query", params=params)
    data = response.json()
    quote = data.get("Global Quote", {})
    price_val = quote.get("05. price", "")

    if not price_val:
        return f"Could not get price for {symbol}. API response: {data}"

    return (
        f"{symbol}: price=${float(price_val):.2f}, "
        f"open=${float(quote.get('02. open', 0)):.2f}, "
        f"high=${float(quote.get('03. high', 0)):.2f}, "
        f"low=${float(quote.get('04. low', 0)):.2f}, "
        f"volume={quote.get('06. volume', '')}, "
        f"change={quote.get('09. change', '')}, "
        f"change_pct={quote.get('10. change percent', '')}"
    )


@mcp.tool()
async def query_db(query: str) -> str:
    names = []
    # """Execute a SELECT query on the MySQL database and return the results."""
    # conn = await aiomysql.connect(**DB_CONFIG)
    # try:
    #     async with conn.cursor(aiomysql.DictCursor) as cursor:
    #         await cursor.execute(query)
    #         rows = await cursor.fetchall()
    # finally:
    #     conn.close()

    # if not rows:
    #     return "Query returned no results."

    # return "\n".join(str(row) for row in rows)
    conn = await asyncpg.connect(
        user=os.getenv("USER"), 
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE"),
        host=os.getenv("DB_HOST"),
        port=5432
    )
    try:
    
    #    async with conn.transaction():
    #      async for record in conn.cursor("SELECT contact_name FROM customers"):
    #          if record["contact_name"] is not None:
    #             names.append(record["contact_name"])
    
         rows = await conn.fetch(query)
    finally:
        await conn.close()

    if not rows:
        return "Query returned no results."

    return "\n".join(str(dict(row)) for row in rows)
    

@mcp.tool()
def write_csv(filename: str, headers: list[str], rows: list[list[str]]) -> str:
    """
    Write data to a CSV file on the server.
    Use this after query_db or price tool calls to save results.
    Pass headers as a list of column names and rows as a list of lists.
    """
    if not filename.endswith(".csv"):
        filename += ".csv"

    filepath = os.path.abspath(filename)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    return f"CSV written successfully: {filepath} ({len(rows)} rows, {len(headers)} columns)"


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Starting MCP server (Streamable HTTP) on http://0.0.0.0:8000")
    print("Clients should connect to: http://localhost:8000/mcp")
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
