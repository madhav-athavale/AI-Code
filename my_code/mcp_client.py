import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_client():
    # 1. Define how to start your server
    server_params = StdioServerParameters(
        command="python3",
        args=["main.py"], # Path to your server file
    )

    # 2. Connect to the server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 3. Initialize the handshake
            await session.initialize()

            # 4. List available tools
            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")

            # 5. Call a tool (e.g., your 'say_hello' tool)
            #result = await session.call_tool("say_hello", arguments={"name": "Madhav"})
            result = await session.call_tool("say_hello", arguments={"name": "Madhav"})
            print(f"Server response: {result.content[0].text}")

if __name__ == "__main__":
    asyncio.run(run_client())