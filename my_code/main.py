# Simple MCP server

from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel,Field

mcp = FastAPI(title="MCP Math and Text Server")

class AddInput(BaseModel):
    a : float = Field(..., description= "First Number")
    b : float = Field(..., description= "Second Number")


@app.get("/tools")
async def list_tools():
    return {
        "tools" : [
            {
                "name" : "add",
                "description": "Add 2 numbers and return sum",
                "inputSchema" : {
                    "type": "object",
                    "properties": {
                        "a" : {"type": "number", "description" : "First Number"},
                        "b" : {"type": "number", "description" : "Second Number"}
                    },
                    "required": ["a","b"]
                }
            }
        ]
    }

@app.post("/tools/add")
async def add_numbers(input_data: AddInput):
    result = input_data.a + input_data.b
    return{
        "content": [
            {
                "type:": "text",
                "text": f"The sum is {result}."
            
            }
        ]
    }
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)