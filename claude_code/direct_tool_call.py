"""
How to call the tool directly, bypassing Claude

Usage:
    python direct_tool_call.py
"""

import asyncio
import pandas as pd
from mcp.client.sse import sse_client
from mcp import ClientSession

SERVER_URL = "http://localhost:8000/sse"


async def write_dataframe_to_csv(df: pd.DataFrame, filename: str):
    async with sse_client(SERVER_URL) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool("write_csv", {
                "filename": filename,
                "headers": df.columns.tolist(),
                "rows":    df.astype(str).values.tolist(),  # all values as strings
            })

            print(result.content[0].text)


# ── Example usage ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Replace this DataFrame with your own
    df = pd.DataFrame({
        "ticker": ["AAPL", "MSFT", "GOOGL"],
        "price":  [189.42, 415.23, 172.55],
        "change": [+1.20, -0.85, +2.10],
    })

    output_file = "/tmp/stocks.csv"   # ← change path as needed

    asyncio.run(write_dataframe_to_csv(df, output_file))
