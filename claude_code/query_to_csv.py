"""
query_to_csv.py
───────────────
Chain pattern:
  1. Claude agent  → runs query_db (interprets natural language → SQL)
  2. Direct call   → write_csv (no Claude, fast and deterministic)

Also supports:
  - get_stock_price → write_csv (same pattern)

Install dependencies:
    pip install "mcp[client]" anthropic httpx-sse pandas python-dotenv

Usage:
    python query_to_csv.py
"""

import asyncio
import json
import pandas as pd
from mcp.client.sse import sse_client
from mcp import ClientSession
import anthropic
from dotenv import load_dotenv

load_dotenv()

SERVER_URL = "http://localhost:8000/sse"
MODEL      = "claude-sonnet-4-6"


def mcp_tools_to_anthropic(mcp_tools):
    return [
        {
            "name":         t.name,
            "description":  t.description,
            "input_schema": t.inputSchema,
        }
        for t in mcp_tools
    ]


# ── Step 1: Use Claude to run query_db and get structured JSON back ────────────
async def fetch_query_results(session: ClientSession, natural_language_query: str) -> dict:
    """
    Ask Claude to interpret a natural language query and call query_db.
    Returns the structured JSON result: {"headers": [...], "rows": [[...]], "count": N}
    """
    mcp_tools = (await session.list_tools()).tools
    tools     = mcp_tools_to_anthropic(mcp_tools)
    client    = anthropic.Anthropic()

    system = (
        "You are a data assistant. When the user asks a database question, "
        "call the query_db tool with the appropriate SQL SELECT query. "
        "Return ONLY the raw tool result — do not summarize or reformat it."
    )
    messages = [{"role": "user", "content": natural_language_query}]

    print(f"  [Agent] Interpreting: '{natural_language_query}'")

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=system,
            tools=tools,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})

        tool_uses = [b for b in response.content if b.type == "tool_use"]
        if not tool_uses:
            break

        tool_results = []
        for tool_use in tool_uses:
            if tool_use.name != "query_db":
                continue  # only care about query_db here
            print(f"  [Agent] Running SQL: {tool_use.input.get('query')}")
            result      = await session.call_tool(tool_use.name, tool_use.input)
            result_text = result.content[0].text
            print(f"  [Agent] Got result ({len(result_text)} bytes)")

            tool_results.append({
                "type":        "tool_result",
                "tool_use_id": tool_use.id,
                "content":     result_text,
            })

            # Parse and return immediately — we have what we need
            return json.loads(result_text)

        messages.append({"role": "user", "content": tool_results})

    raise RuntimeError("Claude did not call query_db for the given query.")


# ── Step 1 (alt): Direct price fetch for one or more tickers ──────────────────
async def fetch_stock_prices(session: ClientSession, tickers: list[str]) -> dict:
    """
    Directly call the price tool for each ticker (no Claude needed).
    Returns structured data: {"headers": [...], "rows": [[...]], "count": N}
    """
    headers = ["ticker", "price", "open", "high", "low", "volume", "change", "change_pct"]
    rows    = []

    for ticker in tickers:
        print(f"  [Direct] Fetching price for {ticker}")
        result      = await session.call_tool("price", {"a": ticker})
        result_text = result.content[0].text
        data        = json.loads(result_text)

        if "error" in data:
            print(f"  [Direct] Warning: {data['error']}")
            continue

        rows.append([str(data.get(h, "")) for h in headers])

    return {"headers": headers, "rows": rows, "count": len(rows)}


# ── Step 2: Direct write_csv call — no Claude ──────────────────────────────────
async def write_csv_direct(session: ClientSession, data: dict, filename: str):
    """
    Directly call write_csv with structured data. No Claude involved.
    data must have keys: headers (list), rows (list of lists)
    """
    print(f"  [Direct] Writing {data['count']} rows to {filename}")
    result = await session.call_tool("write_csv", {
        "filename": filename,
        "headers":  data["headers"],
        "rows":     data["rows"],
    })
    print(f"  [Direct] {result.content[0].text}")


# ── Helper to also return a DataFrame ─────────────────────────────────────────
def to_dataframe(data: dict) -> pd.DataFrame:
    return pd.DataFrame(data["rows"], columns=data["headers"])


# ── Main orchestrator ──────────────────────────────────────────────────────────
async def main():
    async with sse_client(SERVER_URL) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # ── Example 1: DB query → CSV ──────────────────────────────────────
            print("\n── Example 1: DB query → CSV ──────────────────────────")
            data = await fetch_query_results(
                session,
                natural_language_query="Get the top 10 customers by total orders",  # ← change this
            )
            df = to_dataframe(data)
            print(f"  DataFrame preview:\n{df.head()}\n")
            await write_csv_direct(session, data, "/tmp/customers.csv")  # ← change path

            # ── Example 2: Stock prices → CSV (fully direct, no Claude) ────────
            print("\n── Example 2: Stock prices → CSV ──────────────────────")
            stock_data = await fetch_stock_prices(
                session,
                tickers=["AAPL", "MSFT", "GOOGL"],   # ← change tickers
            )
            df2 = to_dataframe(stock_data)
            print(f"  DataFrame preview:\n{df2}\n")
            await write_csv_direct(session, stock_data, "/tmp/stocks.csv")  # ← change path


if __name__ == "__main__":
    asyncio.run(main())
