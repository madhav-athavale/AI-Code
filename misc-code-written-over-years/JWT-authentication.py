#Notes in jwt-authentication-doc.txt file

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timedelta

app = FastAPI()
security = HTTPBearer()

SECRET = "my_secret_key"

@app.post("/login")
def login():
    payload = {"user": "madhav", "exp": datetime.utcnow() + timedelta(minutes=30)}
    token = jwt.encode(payload, SECRET, algorithm="HS256")
    return {"token": token}

@app.get("/protected")
def protected(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        decoded = jwt.decode(credentials.credentials, SECRET, algorithms=["HS256"])
        return {"message": "Access granted", "user": decoded["user"]}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")