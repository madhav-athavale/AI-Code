import os
import platform
import sys
from fastmcp import FastMCP
from duckduckgo_search import DDGS

# Prevent any extra text from breaking the JSON communication pipe
os.environ["FASTMCP_NO_BANNER"] = "1"

mcp = FastMCP("ClaudeServer")

@mcp.tool()
async def search_web(query: str, max_results: int = 5):
    """
    Searches the web for the latest information. 
    Use this for coding help, news, or fact-checking.
    """
    try:
        results = []
        with DDGS() as ddgs:
            # We use the .text method for standard web searches
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title"),
                    "link": r.get("href"),
                    "snippet": r.get("body")
                })
        return results
    except Exception as e:
        return f"Search failed: {str(e)}"

@mcp.tool()
async def add_numbers(a: float, b: float):
    """Adds two numbers and returns the sum."""
    return f"The result is {a + b}"

@mcp.tool()
async def get_sys_info():
    """Returns the user's specific macOS version and hardware details."""
    mac_version = platform.mac_ver()[0]
    os_name = "macOS Tahoe" if mac_version.startswith("26") else "macOS"
    return {
        "os_name": os_name,
        "version": mac_version,
        "machine": platform.machine()
    }

if __name__ == "__main__":
    # This keeps the server waiting for Claude's commands
    mcp.run()