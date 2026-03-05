import asyncio
import os
import platform
import sys
from fastmcp import FastMCP, Client
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")


# --- 1. SETUP THE SERVER ---
mcp_server = FastMCP("SafeTerminalServer")

@mcp_server.tool()
async def add_numbers(a: float, b: float):
    """Adds two numbers and returns the sum."""
    return f"The result is {a + b}"

@mcp_server.tool()
async def get_sys_info():
    """Returns Mac system details."""
    mac_version = platform.mac_ver()[0]
    # Identifying the 2026 version name for Gemini
    os_name = "macOS Tahoe" if mac_version.startswith("26") else "macOS"
    
    return {
        "os_name": os_name,
        "version": mac_version,
        "kernel": f"Darwin {platform.release()}",
        "machine": platform.machine(),
        "hostname": platform.node()
    }

# --- 2. THE CLIENT LOGIC ---
async def main():
  
    api_key = gemini_api_key
    model_id = "gemini-2.5-flash-lite" # Use gemini-3-flash-preview for even better reasoning

    mcp_client = Client(mcp_server)
    genai_client = genai.Client(api_key=api_key)

    async with mcp_client:
        # Fetch tool definitions from the server
        mcp_tools = await mcp_client.list_tools()
        
        user_input = "Add 123 and 456, then check my Mac version."
        print(f"User Request: {user_input}")

        # FIX: Use types.Part(text=...) with keyword argument
        messages = [types.Content(role="user", parts=[types.Part(text=user_input)])]

        # Multi-turn execution loop
        while True:
            response = await genai_client.aio.models.generate_content(
                model=model_id,
                contents=messages,
                config=types.GenerateContentConfig(tools=mcp_tools)
            )

            # Extract parts from the candidate
            model_parts = response.candidates[0].content.parts
            
            # If the model replies with text, we are done
            if any(p.text for p in model_parts):
                print(f"\nGemini Final Response:\n{response.text}")
                break

            # If the model requests tool calls
            messages.append(response.candidates[0].content)
            
            tool_responses = []
            for part in model_parts:
                if part.function_call:
                    name = part.function_call.name
                    args = part.function_call.args
                    
                    print(f"-> Executing: {name}({args})")
                    
                    # Call the tool through the MCP bridge
                    result = await mcp_client.call_tool(name, args)
                    
                    # Format the response for Gemini
                    tool_responses.append(
                        types.Part.from_function_response(
                            name=name,
                            response={"result": result.content[0].text if hasattr(result, 'content') else str(result)}
                        )
                    )

            # Add the tool results to the conversation history
            messages.append(types.Content(role="tool", parts=tool_responses))

if __name__ == "__main__":
    asyncio.run(main())