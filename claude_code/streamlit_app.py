"""
Streamlit UI for MCP Agentic AI
Connects to the StreamableHTTP MCP server and shows the full agent trace.

Install dependencies:
    pip install streamlit "mcp[client]" anthropic python-dotenv

Run:
    streamlit run streamlit_app.py
"""

import asyncio
import json
import streamlit as st
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
import anthropic
from dotenv import load_dotenv

load_dotenv()

# ── Config ─────────────────────────────────────────────────────────────────────
SERVER_URL = "http://localhost:8000/mcp"
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

TOOL_COLORS = {
    "add":       "#22c55e",
    "subtract":  "#ef4444",
    "price":     "#f59e0b",
    "query_db":  "#3b82f6",
    "write_csv": "#8b5cf6",
}


# ── Helpers ────────────────────────────────────────────────────────────────────
def mcp_tools_to_anthropic(mcp_tools):
    return [
        {
            "name":         t.name,
            "description":  t.description,
            "input_schema": t.inputSchema,
        }
        for t in mcp_tools
    ]


def tool_badge(name: str) -> str:
    color = TOOL_COLORS.get(name, "#6b7280")
    return f'<span style="background:{color};color:white;padding:2px 10px;border-radius:999px;font-size:12px;font-weight:600;">{name}</span>'


# Async generator for streaming agent progress to UI
async def run_agent(user_message: str):
    """
    Async generator that yields step dicts as the agent runs.
    Each step has a 'type' of: tool_call | tool_result | final
    """
    async with streamablehttp_client(SERVER_URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            mcp_tools = (await session.list_tools()).tools
            tools     = mcp_tools_to_anthropic(mcp_tools)
            client    = anthropic.Anthropic()
            messages  = [{"role": "user", "content": user_message}]

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
                    final_text = " ".join(
                        b.text for b in response.content if hasattr(b, "text")
                    )
                    yield {"type": "final", "text": final_text}
                    break

                # Yield each step for live UI updates
                tool_results = []
                for tool_use in tool_uses:
                    yield {"type": "tool_call", "name": tool_use.name, "input": tool_use.input}

                    result      = await session.call_tool(tool_use.name, tool_use.input)
                    result_text = " ".join(
                        c.text for c in result.content if hasattr(c, "text")
                    )
                    yield {"type": "tool_result", "name": tool_use.name, "result": result_text}

                    tool_results.append({
                        "type":        "tool_result",
                        "tool_use_id": tool_use.id,
                        "content":     result_text,
                    })

                messages.append({"role": "user", "content": tool_results})


def render_step(step: dict):
    """Render a single agent step in the Streamlit UI."""

    if step["type"] == "tool_call":
        with st.container(border=True):
            st.markdown(
                f"⚙️ **Calling tool** &nbsp; {tool_badge(step['name'])}",
                unsafe_allow_html=True,
            )
            st.json(step["input"])

    elif step["type"] == "tool_result":
        with st.container(border=True):
            st.markdown(
                f"✅ **Result** &nbsp; {tool_badge(step['name'])}",
                unsafe_allow_html=True,
            )
            # Try to pretty-print JSON, fall back to plain text
            try:
                st.json(json.loads(step["result"]))
            except (json.JSONDecodeError, TypeError):
                st.code(step["result"])

    elif step["type"] == "final":
        st.success(step["text"])


# ── Streamlit UI ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="MCP Agentic AI", page_icon="🤖", layout="wide")

st.title("🤖 MCP Agentic AI")
st.caption(f"Connected to `{SERVER_URL}`")

# Tool legend
cols = st.columns(len(TOOL_COLORS))
for col, (name, color) in zip(cols, TOOL_COLORS.items()):
    col.markdown(
        f'<div style="background:{color};color:white;text-align:center;padding:4px 0;'
        f'border-radius:6px;font-size:13px;font-weight:600;">{name}</div>',
        unsafe_allow_html=True,
    )

st.divider()

# Example queries
st.markdown("**Try an example:**")
examples = [
    "Add 142 and 389 then subtract 75",
    "Get stock price for AAPL and MSFT",
    "Get top 5 customers from the database",
    "Get AAPL and MSFT prices and save to /tmp/stocks.csv",
    "Query all products and export to /tmp/products.csv",
]
example_cols = st.columns(len(examples))
for col, ex in zip(example_cols, examples):
    if col.button(ex, use_container_width=True):
        st.session_state["query"] = ex

# Query input
query = st.text_input(
    "Enter your query",
    value=st.session_state.get("query", ""),
    placeholder="e.g. Get AAPL stock price and save to /tmp/stocks.csv",
    key="query",
)

run_btn = st.button("▶ Run", type="primary", disabled=not query)

# Chat history in session state
if "history" not in st.session_state:
    st.session_state.history = []

# Run agent
if run_btn and query:
    st.session_state.history.append({"role": "user", "query": query, "steps": []})

    st.markdown("### Agent Trace")
    steps_container = st.empty()

    # Collect steps and render live
    steps = []

    async def collect():
        async for step in run_agent(query):
            steps.append(step)
            with steps_container.container():
                for s in steps:
                    render_step(s)

    asyncio.run(collect())
    st.session_state.history[-1]["steps"] = steps

# Show past queries
if len(st.session_state.history) > 1:
    st.divider()
    st.markdown("### History")
    for item in reversed(st.session_state.history[:-1]):
        with st.expander(f"🔍 {item['query']}"):
            for s in item["steps"]:
                render_step(s)
