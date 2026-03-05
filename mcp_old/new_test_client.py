import asyncio
import sys
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")


async def main():
    # 1. Point to your server file using the current Python executable
    server_path = "/Users/madhavathavale/workspace/MacMiniM2/mcp/servers/terminal_server/new_terminal_server.py"
    
    # Check if file exists to avoid confusing errors
    if not os.path.exists(server_path):
        print(f"Error: {server_path} not found!")
        return

    # 2. Setup transport - Using sys.executable is the safest way on Mac
    transport = StdioTransport(command=sys.executable, args=[server_path])
    mcp_client = Client(transport)
    
    # 3. Initialize Gemini
    genai_client = genai.Client(api_key=gemini_api_key)

    print("--- Connecting to MCP Server ---")
    
    async with mcp_client:
        # Prompt designed to test multiple tools at once
        user_input = "Add 123 and 456, then tell me what my Mac version is."
        
        print(f"User: {user_input}")
        
        # 4. Generate content with tools enabled
        response = await genai_client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_input,
            config={'tools': mcp_client.tools}
        )

        print(f"\nGemini Response:\n{response.text}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass





