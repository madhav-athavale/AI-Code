from fastapi import FastAPI
from fastmcp import FastMCP
import uvicorn

# 1. Initialize FastMCP
mcp = FastMCP("Math Server")

@mcp.tool()
def add(a: float, b: float) -> str:
    return f"The sum is {a + b}"

@mcp.tool()
def reverse(a: str) -> str:
    """reverse string."""
    return f"The reveser string is {a[::-1]}."
    
# 2. Create the MCP HTTP app first
mcp_app = mcp.http_app(path="/mcp")

# 3. CRITICAL: Pass the mcp_app lifespan to the main FastAPI app
app = FastAPI(
    title="Stable Math Server",
    lifespan=mcp_app.lifespan  # <--- THIS IS THE FIX
)

# 4. Mount it
app.mount("/mcp_server", mcp_app)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)