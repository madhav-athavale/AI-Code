import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def run_math_client():
    # 1. Point to your FastAPI server's SSE route
    # If you used mcp.run(transport="sse"), the default path is /sse
    url = "http://0.0.0.0:8080/sse"
    
    print(f"Connecting to MCP Server at {url}...")

    try:
        # 2. Establish the SSE connection
        # The sse_client context manager handles both the GET stream 
        # and the POST message channel for you automatically.
        async with sse_client(url) as (read_stream, write_stream):
            
            # 3. Create the MCP Session
            async with ClientSession(read_stream, write_stream) as session:
                
                # 4. Perform the Handshake (Mandatory)
                await session.initialize()
                print("Connection initialized successfully!")

                # 5. List Tools to verify the server is responding
                tools = await session.list_tools()
                print(f"Available tools: {[t.name for t in tools.tools]}")

                # 6. Call the 'add' tool
                print("\nCalling 'add' tool with {a: 5, b: 10}...")
                result = await session.call_tool("add", arguments={"a": 15, "b": 17})
                
                # 7. Print the output
                # result.content is a list of content blocks (usually TextContent)
                print(f"Server Response: {result.content[0].text}")

                print("\nCalling 'reverse' tool with {a: 'ABCDE'}...")
                result1 = await session.call_tool("reverse", arguments={"a": "ABCDE"})
                
                # 7. Print the output
                # result.content is a list of content blocks (usually TextContent)
                print(f"Server Response: {result1.content[0].text}")

    except Exception as e:
        print(f"Client Error: {e}")

if __name__ == "__main__":
    asyncio.run(run_math_client())