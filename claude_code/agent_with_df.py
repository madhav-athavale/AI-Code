"""
From Claude
Claude reads the data and decides how to call write_csv.

Install dependencies:
    pip install "mcp[client]" anthropic httpx-sse pandas

Usage:
    python agent_with_df.py
"""

import asyncio
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


async def run_agent_with_df(df: pd.DataFrame, filename: str, instructions: str = ""):
    """
    Pass a DataFrame to the Claude agent.
    Claude will use write_csv to save it based on the instructions.

    Args:
        df:           The pandas DataFrame to write
        filename:     Where to save the CSV
        instructions: Optional extra instruction for Claude
    """
    # Serialize DataFrame as JSON for Claude to understand and manipulate
    data_json = df.to_json(orient="records", indent=2)
    columns   = df.columns.tolist()

    prompt = f"""
Write the following data to a CSV file.

Filename: {filename}
Columns: {columns}
Data (JSON):
{data_json}

{instructions}

Use the write_csv tool with the exact columns as headers and each record as a row.
"""

    async with sse_client(SERVER_URL) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            mcp_tools = (await session.list_tools()).tools
            tools     = mcp_tools_to_anthropic(mcp_tools)
            client    = anthropic.Anthropic()
            messages  = [{"role": "user", "content": prompt}]

            print(f"\nSending DataFrame ({len(df)} rows x {len(df.columns)} cols) to agent...")
            print(f"Target file: {filename}\n")

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
                            print(f"Agent: {block.text}")
                    break

                tool_results = []
                for tool_use in tool_uses:
                    print(f"[Tool call] {tool_use.name}({tool_use.input})")
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


# ── Example usage ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Replace this DataFrame with your own
    df = pd.DataFrame({
        "customer_id":   [1, 2, 3],
        "name":          ["Alice Johnson", "Bob Smith", "Carol White"],
        "email":         ["alice@example.com", "bob@example.com", "carol@example.com"],
        "total_orders":  [12, 5, 8],
        "revenue":       [2400.50, 875.00, 1650.75],
    })

    output_file  = "/tmp/customers.csv"       # ← change path as needed
    instructions = "Sort the rows by revenue descending before writing."  # ← optional

    asyncio.run(run_agent_with_df(df, output_file, instructions))
