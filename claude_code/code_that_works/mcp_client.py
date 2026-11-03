"""
MCP Client - Agentic AI Template (Streamable HTTP) — mcp SDK v2
Connects to a running MCP server over HTTP, with an optional Skill layered
on top for workflow guidance (e.g. the "stock-report" skill).

Everything stays local: this script talks to your MCP server on localhost
directly (client-side tool orchestration), and the Skill itself runs in
Anthropic's cloud sandbox. No tunnel/ngrok needed for this setup.

Install dependencies:
    pip install "mcp>=2,<3" anthropic python-dotenv

Usage:
    python mcp_client.py
"""

import asyncio
import os
from mcp.client.streamable_http import streamable_http_client  # v2: renamed from streamablehttp_client
from mcp import ClientSession
import anthropic
from dotenv import load_dotenv

load_dotenv()

# ── Config ───────────────────────────────────────────────────────────────────
SERVER_URL = "http://localhost:8000/mcp"   # Streamable HTTP's single endpoint
#MODEL = "claude-sonnet-4-6"
MODEL="claude-haiku-4-5-20251001"

# Set this to your uploaded custom skill's ID (e.g. "skill_01AbCdEfGhIjKlMnOpQrStUv").
# Leave as None to run without a skill layer.
SKILL_ID = os.getenv("STOCK_REPORT_SKILL_ID")  # or hardcode the skill_ you got back

SYSTEM = (
    "You are a helpful data assistant with access to tools for math, "
    "stock prices, and a MySQL database. "
    "When the user asks to save, export, or write results to CSV, "
    "use the write_csv tool. For database query results, extract the "
    "column names as headers and each row's values as CSV rows. "
    "For stock price results, use headers like ['Ticker', 'Price'] and "
    "one row per stock. Always confirm the file was written."
)


# ── Convert MCP tools → Anthropic format ────────────────────────────────────
def mcp_tools_to_anthropic(mcp_tools):
    return [
        {
            "name": t.name,
            "description": t.description,
            "input_schema": t.input_schema,  # v2: inputSchema -> input_schema
        }
        for t in mcp_tools
    ]


# ── Agentic loop ─────────────────────────────────────────────────────────────
async def run_agent(user_message: str):
    # *_ absorbs the extra return value regardless of whether the installed
    # version still yields a get_session_id callback as a 3rd item
    async with streamable_http_client(SERVER_URL) as (read, write, *_):
        async with ClientSession(read, write) as session:
            await session.initialize()

            mcp_tools = (await session.list_tools()).tools
            tools = mcp_tools_to_anthropic(mcp_tools)
            client = anthropic.Anthropic()
            messages = [{"role": "user", "content": user_message}]

            print(f"\n{'=' * 50}")
            print(f"User: {user_message}")
            print(f"{'=' * 50}")

            # Skills require the code execution tool (it's the sandbox Skills
            # run in). It's harmless to include even if SKILL_ID is unset.
            request_tools = tools + [{"type": "code_execution_20250825", "name": "code_execution"}]

            request_kwargs = dict(
                model=MODEL,
                # 1024 was too small: a tool_use call embedding a full query_db
                # result (e.g. all rows for write_csv) can easily exceed that,
                # causing the response to cut off mid-JSON with fields like
                # "rows" missing entirely. Raised to give room for larger payloads.
                max_tokens=8192,
                system=SYSTEM,
                tools=request_tools,
                betas=["code-execution-2025-08-25"],
            )

            if SKILL_ID:
                request_kwargs["betas"].append("skills-2025-10-02")
                request_kwargs["container"] = {
                    "skills": [{"type": "custom", "skill_id": SKILL_ID, "version": "latest"}]
                }

            while True:
                response = client.beta.messages.create(
                    messages=messages,
                    **request_kwargs,
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
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": result_text,
                    })

                messages.append({"role": "user", "content": tool_results})


# ── Entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    while True:
        query = input("\nEnter Query (or 'quit' to exit): ").strip()
        if query.lower() in ("quit", "exit", "q"):
            break
        if query:
            asyncio.run(run_agent(query))