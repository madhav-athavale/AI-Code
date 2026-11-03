from fastapi import FastAPI, Depends, Header, HTTPException
import uvicorn
# 1. Initialize the FastAPI app
app = FastAPI(title="Header Authentication Example")

# 2. Define the dependency function
async def verify_token(x_token: str = Header(..., description="You must enter 'secret-token' here")):
    if x_token != "secret-token":
        raise HTTPException(status_code=400, detail="Invalid Token")

# 3. A public route for comparison (No dependency)
@app.get("/")
async def public_route():
    return {"message": "Anyone can see this route!"}

# 4. The protected route (Requires the dependency)
@app.get("/protected-route")
async def get_protected_data(auth: None = Depends(verify_token)):
    return {"data": "Secret information"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port = 8000)