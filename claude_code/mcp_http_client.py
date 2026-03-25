"""
Fom Claude
MCP StreamableHTTP Client - Agentic AI Template
Connects to the StreamableHTTP server via single /mcp endpoint.

Install dependencies:
    pip install "mcp[client]" anthropic python-dotenv

Changes from SSE version:
    SSE:  from mcp.client.sse import sse_client
          async with sse_client(url) as (read, write):

    HTTP: from mcp.client.streamable_http import streamablehttp_client
          async with streamablehttp_client(url) as (read, write, _):
          NOTE: returns 3 values — third (_) is get_session_id callable, safe to ignore

Usage:
    python mcp_http_client.py
"""

import asyncio
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
import anthropic
from dotenv import load_dotenv

load_dotenv()

# ── Config ─────────────────────────────────────────────────────────────────────
SERVER_URL = "http://localhost:8000/mcp"   # single endpoint
MODEL      = "claude-sonnet-4-6"

SYSTEM = (
    "You are a helpful data assistant with access to tools for math, "
    "stock prices, and a MySQL database. "
    "When the user asks to save, export, or write results to CSV, "
    "use the write_csv tool. For database query results, extract the "
    "column names as headers and each row's values as CSV rows. "
    "For stock price results, use headers like ['Ticker', 'Price'] and "
    "one row per stock. Always confirm the file was written."
)


# ── Convert MCP tools → Anthropic format ──────────────────────────────────────
def mcp_tools_to_anthropic(mcp_tools):
    return [
        {
            "name":         t.name,
            "description":  t.description,
            "input_schema": t.inputSchema,
        }
        for t in mcp_tools
    ]


# ── Agentic loop ───────────────────────────────────────────────────────────────
async def run_agent(user_message: str):
    # Returns (read, write, get_session_id) — third value ignored with _
    async with streamablehttp_client(SERVER_URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            mcp_tools = (await session.list_tools()).tools
            tools     = mcp_tools_to_anthropic(mcp_tools)
            client    = anthropic.Anthropic()
            messages  = [{"role": "user", "content": user_message}]

            print(f"\n{'='*50}")
            print(f"User: {user_message}")
            print(f"{'='*50}")

            while True:
                response = client.messages.create(
                    model=MODEL,
                    max_tokens=1024,
                    system=SYSTEM,
                    tools=tools,
                    messages=messages,
                )

                messages.append({"role": "assistant", "content": response.content})

                tool_uses = [b for b in response.content if b.type == "tool_use"]

                if not tool_uses:
                    for block in response.content:
                        if hasattr(block, "text"):
                            print(f"\nAssistant: {block.text}")
                    break

                tool_results = []
                for tool_use in tool_uses:
                    print(f"\n[Tool call] {tool_use.name}({tool_use.input})")
                    result = await session.call_tool(tool_use.name, tool_use.input)

                    result_text = " ".join(
                        c.text for c in result.content if hasattr(c, "text")
                    )
                    print(f"[Tool result] {result_text}")

                    tool_results.append({
                        "type":        "tool_result",
                        "tool_use_id": tool_use.id,
                        "content":     result_text,
                    })

                messages.append({"role": "user", "content": tool_results})


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    while True:
        query = input("\nEnter Query (or 'quit' to exit): ").strip()
        if query.lower() in ("quit", "exit", "q"):
            break
        if query:
            asyncio.run(run_agent(query))
