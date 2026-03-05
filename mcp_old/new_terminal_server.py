import os
import sys
import platform
import subprocess
from fastmcp import FastMCP

# 1. PREVENT BANNER: This is the most important fix for 'Connection closed'
os.environ["FASTMCP_NO_BANNER"] = "1"

mcp = FastMCP("SafeTerminalServer")

# Helper to print debug info without breaking the protocol
def log(msg):
    print(f"DEBUG: {msg}", file=sys.stderr)

@mcp.tool()
async def add_numbers(a: float, b: float, **kwargs):
    """Adds two numbers."""
    log(f"Adding {a} + {b}")
    return f"The result is {a + b}"

@mcp.tool()
async def get_sys_info(**kwargs):
    """Returns Mac system details."""
    return f"Host: {platform.node()}, OS: {platform.system()} {platform.mac_ver()[0]}"

@mcp.tool()
async def list_files(path: str = ".", **kwargs):
    """Lists files safely."""
    try:
        files = os.listdir(path)
        return f"Files: {', '.join(files)}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Ensure we run in stdio mode without any extra noise
    mcp.run(transport="stdio")