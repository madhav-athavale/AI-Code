"""
MCP Server - Agentic AI Template
Exposes 'add' and 'subtract' as MCP tools.
"""

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import json
import requests
import httpx
import aiomysql
# Initialize MCP server
app = Server("calculator-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """Register available tools."""
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
            description="find stock price",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "string", "description": "Ticker"},
                },
                "required": ["a"],
            },
        ),

        Tool(
            name = "qu",
            description="Execute a mysql select query",
            inputSchema={
                "type": "object",
                "properties" :{
                    "query": {"type": "string", "description": "SQL QUERY"}
                },

                "required": ["query"],

            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Route tool calls to their implementations."""

    if name == "add":
        a = arguments["a"]
        b = arguments["b"]
        result = a + b
        return [TextContent(type="text", text=f"{a} + {b} = {result}")]

    elif name == "subtract":
        a = arguments["a"]
        b = arguments["b"]
        result = a - b
        return [TextContent(type="text", text=f"{a} - {b} = {result}")]
    elif name == "qu":
        query = arguments["query"]

        # TODO: Move credentials to .env
        conn = await aiomysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="Pma94029@",
            db="northwind"

        )

        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(query)
            rows = await cursor.fetchall()
        conn.close()
        if not rows:
            return [TextContent(type="text", text="Query returned no results.")]

        result = "\n".join(str(row) for row in rows)
        return [TextContent(type="text", text=f"Query results:\n{result}")]


    elif name == "price":

        symbol = arguments["a"]
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": "A6QAMSHO0IPIOIR0"   # TODO: Move to .env
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
        
        data = response.json()
        quote = data.get("Global Quote", {})
        price = quote.get("05. price", "")

        # if not price:
        #     return [TextContent(type="text", text=f"Could not get price. API response: {data}")]

        return [TextContent(type="text", text=f"STATUS={response.status_code} BODY={response.text}")]
        #return [TextContent(type="text", text=f"The current price of {symbol} is ${float(price):.2f}")]
    else:
            raise ValueError(f"Unknown tool: {name}")


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
