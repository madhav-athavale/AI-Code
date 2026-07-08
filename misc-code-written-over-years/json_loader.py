import json

from fastapi import FastAPI

from pydantic import BaseModel


app = FastAPI()

@app.get("/group/{id}")
def read_item(id:int):
    # item_id is validated as an integer automatically
    return {"id" :id}
 

