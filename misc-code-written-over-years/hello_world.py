# Basic MCP Server
from fastmcp import FastMCP

# 1. Initialize the Server
mcp = FastMCP("MyFirstServer")

# 2. Add a Tool
@mcp.tool()
def say_hello(name: str) -> str:
    """
    Greets a user by name. 
    The AI will see this docstring to understand what the tool does.
    """
    return f"Hello, {name}! Your M4 Mac Mini says hi."

# 3. Run the Server
if __name__ == "__main__":
    mcp.run()
    #await mcp.run_async()