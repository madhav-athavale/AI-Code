# Save this as math_server.py
from fastmcp import FastMCP

from fastapi import FastAPI
import uvicorn

app = FastAPI()

mcp = FastMCP("Math Server")

@mcp.tool()
def add(a: float, b: float) -> str:
    """Add two numbers and return the sum."""
    return f"The sum is {a + b}."

@mcp.tool()
def reverse(a: str) -> str:
    """reverse string."""
    return f"The reveser string is {a[::-1]}."

mcp_app = mcp.http_app(path="/mcp")
app.mount("/mcp_server", mcp_app)
if __name__ == "__main__":
    # This MUST match the transport the client expects
    uvicorn.run(app,host="0.0.0.0", port=8080)