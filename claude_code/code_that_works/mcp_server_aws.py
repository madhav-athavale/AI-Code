"""
MCP Server - Agentic AI Template (MCPServer + Streamable HTTP) — mcp SDK v2
Runs as a standalone HTTP server supporting multiple clients.
Tools: add, subtract, price (Alpha Vantage), query_db, list_tables,
       describe_table (PostgreSQL), write_csv, export_query_to_csv

Install dependencies:
    pip install "mcp>=2,<3" httpx asyncpg python-dotenv

Run:
    python mcp_server.py
Clients connect to:
    http://localhost:8000/mcp
"""

import os
import csv
import httpx
import asyncpg
from dotenv import load_dotenv
from mcp.server.mcpserver import MCPServer

load_dotenv()

# v2: host/port are no longer constructor args — they move to run()
mcp = MCPServer("calculator-server")

AV_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),  # asyncpg uses "database", not "db"
}

OUTPUT_DIR = os.getenv("OUTPUT_DIR", os.path.abspath("output"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

def safe_path(filename: str) -> str:
    if not filename.endswith(".csv"):
        filename += ".csv"
    return os.path.join(OUTPUT_DIR, os.path.basename(filename))

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
    """Execute a SELECT query on the PostgreSQL database and return the results."""
    conn = await asyncpg.connect(**DB_CONFIG)
    try:
        rows = await conn.fetch(query)
    finally:
        await conn.close()

    if not rows:
        return "Query returned no results."

    return "\n".join(str(dict(row)) for row in rows)


@mcp.tool()
async def list_tables() -> str:
    """
    List all table names in the public schema.
    Call this first if you're unsure what tables exist before writing a query.
    """
    conn = await asyncpg.connect(**DB_CONFIG)
    try:
        rows = await conn.fetch(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
            """
        )
    finally:
        await conn.close()

    if not rows:
        return "No tables found in the public schema."

    return "\n".join(r["table_name"] for r in rows)


@mcp.tool()
async def describe_table(table_name: str) -> str:
    """
    Get column names and data types for a specific table.
    Call this before writing a query if you're unsure of a table's exact
    column names (e.g. whether it's 'name' or 'customer_name').
    """
    conn = await asyncpg.connect(**DB_CONFIG)
    try:
        rows = await conn.fetch(
            """
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = $1
            ORDER BY ordinal_position
            """,
            table_name,
        )
    finally:
        await conn.close()

    if not rows:
        return f"No columns found for table '{table_name}'. It may not exist — try list_tables first."

    lines = [f"{r['column_name']}: {r['data_type']} (nullable={r['is_nullable']})" for r in rows]
    return "\n".join(lines)


@mcp.tool()
def write_csv(filename: str, headers: list[str], rows: list[list[str]]) -> str:
    """
    Write data to a CSV file on the server.
    Use this when the data has already been seen/transformed by the model
    (e.g. after price, or after filtering/reshaping query_db results) — the
    caller must supply the actual row data as 'rows'.

    For exporting a raw query result straight to CSV with no transformation,
    use export_query_to_csv instead — it's much faster since the row data
    never has to be generated as model output.
    """
    if not filename.endswith(".csv"):
        filename += ".csv"

    filepath = safe_path(filename)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    return f"CSV written successfully: {filepath} ({len(rows)} rows, {len(headers)} columns)"


@mcp.tool()
async def export_query_to_csv(query: str, filename: str) -> str:
    """
    Run a SELECT query and write the results directly to a CSV file on the
    server, without the row data passing through the conversation. Prefer
    this over query_db + write_csv whenever the request is a straight export
    with no filtering/transformation needed — it's much faster for large
    results since the model never has to re-generate the row data as output.
    """
    if not filename.endswith(".csv"):
        filename += ".csv"

    conn = await asyncpg.connect(**DB_CONFIG)
    try:
        rows = await conn.fetch(query)
    finally:
        await conn.close()

    if not rows:
        return "Query returned no results — no file written."

    headers = list(rows[0].keys())
    filepath = safe_path(filename)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in rows:
            writer.writerow([str(v) for v in row.values()])

    return f"CSV written successfully: {filepath} ({len(rows)} rows, {len(headers)} columns)"


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Starting MCP server (Streamable HTTP) on http://0.0.0.0:8000")
    print("Clients should connect to: http://localhost:8000/mcp")
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
