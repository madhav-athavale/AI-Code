"""
MCP SSE Client - Agentic AI Template
Connects to a running MCP SSE server over HTTP.

Install dependencies:
    pip install "mcp[client]" anthropic httpx-sse

Usage:
    python mcp_sse_client.py
"""

import asyncio
import os
from mcp.client.sse import sse_client
from mcp import ClientSession
import anthropic

from dotenv import load_dotenv

load_dotenv()
# ── Config ─────────────────────────────────────────────────────────────────────
SERVER_URL = "http://localhost:8000/sse"   # Update if server is on another machine
MODEL      = "claude-sonnet-4-6"


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
    async with sse_client(SERVER_URL) as (read, write):
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
