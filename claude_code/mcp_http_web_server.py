"""
MCP StreamableHTTP Server - Agentic AI Template
Single /mcp endpoint handles everything.
Tools: add, subtract, price (Alpha Vantage), query_db (MySQL), write_csv, web_search (Brave)

Install dependencies:
    pip install fastmcp uvicorn httpx aiomysql python-dotenv

Get a free Brave Search API key at:
    https://api.search.brave.com/register
Then add to your .env:
    BRAVE_API_KEY=your_key_here
"""

import csv
import json
import os
import httpx
import aiomysql
import uvicorn

from fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

# ── Config ─────────────────────────────────────────────────────────────────────
AV_API_KEY   = os.getenv("ALPHAVANTAGE_API_KEY")
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")

DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "port":     int(os.getenv("DB_PORT", 3306)),
    "user":     os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "db":       os.getenv("DB_NAME"),
}

# ── FastMCP server ─────────────────────────────────────────────────────────────
mcp = FastMCP("calculator-server")


# ── Tools ──────────────────────────────────────────────────────────────────────
@mcp.tool()
def add(a: float, b: float) -> str:
    """Adds two numbers together."""
    return f"{a} + {b} = {a + b}"


@mcp.tool()
def subtract(a: float, b: float) -> str:
    """Subtracts the second number from the first."""
    return f"{a} - {b} = {a - b}"


@mcp.tool()
async def price(a: str) -> str:
    """Find the current stock price for a ticker symbol (e.g. MSFT, AAPL)."""
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol":   a,
        "apikey":   AV_API_KEY,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get("https://www.alphavantage.co/query", params=params)
    data  = response.json()
    quote = data.get("Global Quote", {})
    p     = quote.get("05. price", "")

    if not p:
        return json.dumps({"error": f"Could not get price for {a}", "raw": data})

    return json.dumps({
        "ticker":     a,
        "price":      round(float(p), 2),
        "open":       round(float(quote.get("02. open", 0)), 2),
        "high":       round(float(quote.get("03. high", 0)), 2),
        "low":        round(float(quote.get("04. low",  0)), 2),
        "volume":     quote.get("06. volume", ""),
        "change":     quote.get("09. change", ""),
        "change_pct": quote.get("10. change percent", ""),
    })


@mcp.tool()
async def query_db(query: str) -> str:
    """Execute a SELECT query on the MySQL database. Returns structured JSON."""
    conn = await aiomysql.connect(**DB_CONFIG)
    async with conn.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(query)
        rows = await cursor.fetchall()
    conn.close()

    if not rows:
        return json.dumps({"columns": [], "rows": [], "row_count": 0})

    columns   = list(rows[0].keys())
    data_rows = [[str(v) for v in row.values()] for row in rows]
    return json.dumps({"columns": columns, "rows": data_rows, "row_count": len(data_rows)})


@mcp.tool()
def write_csv(filename: str, headers: list[str], rows: list[list[str]]) -> str:
    """
    Write data to a CSV file on the server.
    filename: output path e.g. /tmp/results.csv
    headers:  list of column names
    rows:     list of rows, each a list of string values
    """
    if not filename.endswith(".csv"):
        filename += ".csv"

    filepath = os.path.abspath(filename)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    return f"CSV written: {filepath} ({len(rows)} rows, {len(headers)} columns)"


@mcp.tool()
async def web_search(query: str, count: int = 5) -> str:
    """
    Search the web using Brave Search API.
    Returns top results with title, url, and description.

    query: search terms e.g. 'Python FastMCP tutorial'
    count: number of results to return (1-10, default 5)
    """
    if not BRAVE_API_KEY:
        return json.dumps({"error": "BRAVE_API_KEY not set in .env"})

    count = max(1, min(count, 10))  # clamp between 1 and 10

    headers = {
        "Accept":              "application/json",
        "Accept-Encoding":     "gzip",
        "X-Subscription-Token": BRAVE_API_KEY,
    }
    params = {
        "q":     query,
        "count": count,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.search.brave.com/res/v1/web/search",
            headers=headers,
            params=params,
        )

    if response.status_code != 200:
        return json.dumps({
            "error":  f"Brave API returned {response.status_code}",
            "detail": response.text,
        })

    data    = response.json()
    results = data.get("web", {}).get("results", [])

    if not results:
        return json.dumps({"query": query, "results": [], "count": 0})

    # Return clean structured results — title, url, description only
    cleaned = [
        {
            "title":       r.get("title", ""),
            "url":         r.get("url", ""),
            "description": r.get("description", ""),
        }
        for r in results
    ]

    return json.dumps({
        "query":   query,
        "count":   len(cleaned),
        "results": cleaned,
    }, indent=2)


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = mcp.http_app()
    print("Starting MCP StreamableHTTP Server on http://0.0.0.0:8000")
    print("Endpoint: http://localhost:8000/mcp")
    print("Tools:    add, subtract, price, query_db, write_csv, web_search")
    uvicorn.run(app, host="0.0.0.0", port=8000)
