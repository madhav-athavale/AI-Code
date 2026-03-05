import asyncio
import sys
import os
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from anthropic import Anthropic

# Replace with your actual key
ANTHROPIC_API_KEY = "XXX"

async def main():
    # 1. Setup the transport to talk to your server file
    # We use sys.executable to ensure it uses your current Python environment
    server_script = "/Users/madhavathavale/workspace/MacMiniM2/mcp/servers/terminal_server/claude_server.py"
    transport = StdioTransport(command=sys.executable, args=[server_script])
    
    mcp_client = Client(transport)
    mcp_client.timeout = 30.0
    anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)

    print(f"--- Connecting to {server_script} ---")
    
    async with mcp_client:
        # Fetch tool definitions and format for Claude
        mcp_tools = await mcp_client.list_tools()
        claude_tools = [{
            "name": t.name,
            "description": t.description,
            "input_schema": t.inputSchema
        } for t in mcp_tools]

        user_input = "what was the Dow Jones Index on Feb 1, 2026 at close"
        messages = [{"role": "user", "content": user_input}]

        while True:
            # Send message to Claude
            response = anthropic_client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1024,
                tools=claude_tools,
                messages=messages
            )

            # Add assistant's response to history
            messages.append({"role": "assistant", "content": response.content})

            # Check if Claude is done or needs a tool
            if response.stop_reason != "tool_use":
                print(f"\nClaude Response:\n{response.content[0].text}")
                break

            # Process tool calls
            for block in response.content:
                if block.type == "tool_use":
                    print(f"-> Executing {block.name}...")
                    
                    # Call the server tool
                    result = await mcp_client.call_tool(block.name, block.input)
                    
                    # Claude results are often nested; we extract the text content
                    
                    # result_text = result.content[0].text if hasattr(result, 'content') else str(result)
                    result_text =  str(result)

                    # Feed the result back to Claude
                    messages.append({
                        "role": "user",
                        "content": [{
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result_text
                        }]
                    })

if __name__ == "__main__":
    asyncio.run(main())