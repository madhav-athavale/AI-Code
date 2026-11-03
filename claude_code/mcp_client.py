"""
MCP Client - Agentic AI Template
Uses Claude + MCP to call add/subtract tools on the server.
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import anthropic
from dotenv import load_dotenv

load_dotenv()

# ── Config ─────────────────────────────────────────────────────────────────────
SERVER_SCRIPT = "/Users/madhavathavale/workspace/MacMiniM2/claude_code/mcp_server.py" 
# Path to your MCP server script
MODEL = "claude-sonnet-4-6"      # Claude model to use


# MCP and Anthropic use slightly different tool schema formats
def mcp_tools_to_anthropic(mcp_tools):
    return [
        {
            "name": t.name,
            "description": t.description,
            "input_schema": t.inputSchema,
        }
        for t in mcp_tools
    ]


# ── Agentic loop ───────────────────────────────────────────────────────────────
async def run_agent(user_message: str):
    server_params = StdioServerParameters(
        command="python", args=[SERVER_SCRIPT]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Fetch tools from the MCP server
            mcp_tools = (await session.list_tools()).tools
            tools     = mcp_tools_to_anthropic(mcp_tools)

            client   = anthropic.Anthropic()
            messages = [{"role": "user", "content": user_message}]

            print(f"\n{'='*50}")
            print(f"User: {user_message}")
            print(f"{'='*50}")

            # Agentic loop: Claude → tool_use → MCP server → tool_result → Claude (repeat until done)
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
                    # No more tool calls → print final answer and stop
                    for block in response.content:
                        if hasattr(block, "text"):
                            print(f"\nAssistant: {block.text}")
                    break

                # Execute each tool call on the MCP server
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

                # Feed tool results back to Claude as next user message
                messages.append({"role": "user", "content": tool_results})


# ── Entry point ────────────────────────────────────────────────────────────────
#if __name__ == "__main__":
    # Example queries — Claude will decide which tools to call
    # queries = [
    #     "What is 42 + 58?",
    #     "Subtract 17 from 100, then add 5 to the result.",
    #     "I have 200 apples. I give away 75, then receive 30 more. How many do I have?",
    # ]

    # for query in queries:
    #     asyncio.run(run_agent(query))
    #     print()
if __name__ == "__main__":
    while True:
        query = input("\nEnter Query (or 'quit' to exit): ").strip()
        if query.lower() in ("quit", "exit", "q"):
            break
        if query:
            asyncio.run(run_agent(query))
