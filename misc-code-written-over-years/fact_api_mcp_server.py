# Simple MCP server
from fastapi import FastAPI
import uvicorn
from fastapi_mcp import FastApiMCP
from fastapi.middleware.cors import CORSMiddleware
app= FastAPI()

@app.post(
    "/subtract"
)

async def subtract(a:float, b: float):
    return a - b

mcp = FastApiMCP(app)
mcp.mount()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port = 8000)
