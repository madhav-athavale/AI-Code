import asyncio
from fastmcp.client import Client

async def main():
    # Point directly to your server URL
    # If using mcp.http_app(path="/mcp") mounted at /mcp_server
    server_url = "http://127.0.0.1:8080/mcp_server/mcp"
    
    print(f"Connecting to: {server_url}")

    try:
        # FastMCP Client handles the Streamable HTTP handshake automatically
        async with Client(server_url) as client:
            print("Connected successfully!")

            # List tools to verify discovery
            tools = await client.list_tools()
            print(f"Available tools: {[t.name for t in tools]}")

            # Call the tool
            result = await client.call_tool("add", {"a": 13.5, "b": 4.5})
            print(f"Tool Result: {result}")

            result = await client.call_tool("reverse", {"a": "XYZ"})
            print(f"Tool Result: {result}")


    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())