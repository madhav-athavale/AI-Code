"""
From Claude
MCP SSE Server - Agentic AI Template
Runs as a standalone HTTP server supporting multiple clients.
Tools: add, subtract, price (Alpha Vantage), query_db (MySQL)

Install dependencies:
    pip install "mcp[server]" uvicorn starlette httpx aiomysql
"""

import uvicorn
import httpx
import aiomysql
import csv
import os as _os
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from mcp.types import Tool, TextContent
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.requests import Request
from dotenv import load_dotenv
import os

load_dotenv()

# ── MCP Server ─────────────────────────────────────────────────────────────────
app = Server("calculator-server")

# ── MySQL config — update these ────────────────────────────────────────────────
DB_CONFIG = {
    "host" : "localhost",
    "port" : 3306,
    "user" : "root",
    "password": "Pma94029@",
    "db": "northwind",
}

# ── Alpha Vantage config ───────────────────────────────────────────────────────
AV_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "port":     int(os.getenv("DB_PORT", 3306)),
    "user":     os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "db":       os.getenv("DB_NAME"),
}


# ── Tool definitions ───────────────────────────────────────────────────────────
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="add",
            description="Adds two numbers together.",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
        ),
        Tool(
            name="subtract",
            description="Subtracts the second number from the first.",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "Number to subtract from"},
                    "b": {"type": "number", "description": "Number to subtract"},
                },
                "required": ["a", "b"],
            },
        ),
        Tool(
            name="price",
            description="Find the current stock price for a ticker symbol.",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "string", "description": "Ticker symbol e.g. MSFT, AAPL"},
                },
                "required": ["a"],
            },
        ),
        Tool(
            name="query_db",
            description="Execute a SELECT query on the MySQL database.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "SQL SELECT query to execute"},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="write_csv",
            description=(
                "Write data to a CSV file on the server. "
                "Use this after query_db or price tool calls to save results. "
                "Pass headers as a list of column names and rows as a list of lists."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Output filename (e.g. results.csv). Saved to current directory.",
                    },
                    "headers": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Column header names",
                    },
                    "rows": {
                        "type": "array",
                        "items": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "description": "List of rows; each row is a list of string values matching the headers",
                    },
                },
                "required": ["filename", "headers", "rows"],
            },
        ),
    ]


# ── Tool execution ─────────────────────────────────────────────────────────────
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:

    if name == "add":
        a, b = arguments["a"], arguments["b"]
        return [TextContent(type="text", text=f"{a} + {b} = {a + b}")]

    elif name == "subtract":
        a, b = arguments["a"], arguments["b"]
        return [TextContent(type="text", text=f"{a} - {b} = {a - b}")]

    elif name == "price":
        symbol = arguments["a"]
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol":   symbol,
            "apikey":   AV_API_KEY,
        }
        async with httpx.AsyncClient() as client:
            response = await client.get("https://www.alphavantage.co/query", params=params)
        data  = response.json()
        quote = data.get("Global Quote", {})
        price = quote.get("05. price", "")

        if not price:
            return [TextContent(type="text", text=f"Could not get price. API response: {data}")]
        return [TextContent(type="text", text=f"The current price of {symbol} is ${float(price):.2f}")]

    elif name == "query_db":
        query = arguments["query"]
        conn  = await aiomysql.connect(**DB_CONFIG)
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(query)
            rows = await cursor.fetchall()
        conn.close()

        if not rows:
            return [TextContent(type="text", text="Query returned no results.")]
        result = "\n".join(str(row) for row in rows)
        return [TextContent(type="text", text=f"Query results:\n{result}")]

    elif name == "write_csv":
        filename = arguments["filename"]
        headers  = arguments["headers"]
        rows     = arguments["rows"]

        # Ensure .csv extension
        if not filename.endswith(".csv"):
            filename += ".csv"

        filepath = _os.path.abspath(filename)
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

        return [TextContent(
            type="text",
            text=f"CSV written successfully: {filepath} ({len(rows)} rows, {len(headers)} columns)",
        )]

    else:
        raise ValueError(f"Unknown tool: {name}")


# ── SSE transport ──────────────────────────────────────────────────────────────
sse = SseServerTransport("/messages/")

async def handle_sse(request: Request):
    async with sse.connect_sse(
        request.scope, request.receive, request._send
    ) as streams:
        await app.run(streams[0], streams[1], app.create_initialization_options())

starlette_app = Starlette(
    routes=[
        Route("/sse", endpoint=handle_sse),
        Mount("/messages/", app=sse.handle_post_message),
    ]
)

# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Starting MCP SSE Server on http://0.0.0.0:8000")
    print("Clients should connect to: http://localhost:8000/sse")
    uvicorn.run(starlette_app, host="0.0.0.0", port=8000)
