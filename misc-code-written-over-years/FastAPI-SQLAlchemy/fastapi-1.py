from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Strings(BaseModel): 
    string_id: str
    string_data: str
    
@app.post("/Strings/")
async def create_item(string: Strings):
    # 'item' is automatically validated as an Item instance.
    # If the client sends 'price': "twenty", FastAPI returns a 422 error automatically.
    return {"string_id": string.string_id, "string_data": string.string_data}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port = 8000)
