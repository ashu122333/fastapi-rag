from typing import Optional
from fastapi import FastAPI, HTTPException
from llm import query

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Define a route without API key protection
@app.post("/query")
async def run_code(data: dict):
    # Extract input data from the request body
    input_data = data.get("input")
    if not input_data:
        raise HTTPException(status_code=400, detail="Input data is required")
    
    # Process the input data and generate output
    output = query(input_data)
    return {"status": "success", "output": output}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}





# from typing import Optional
# from fastapi import FastAPI
# from fastapi import FastAPI, HTTPException, Depends, Request
# from fastapi.security import APIKeyHeader
# from llm import query

# app = FastAPI()

# API_KEY = "3690"
# API_KEY_NAME = "X-API-Key"

# # Dependency to check the API key in the request header
# api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# def verify_api_key(api_key: str = Depends(api_key_header)):
#     if api_key != API_KEY:
#         raise HTTPException(status_code=403, detail="Invalid or missing API Key")


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

# # Define a route with API key protection
# @app.post("/query")
# async def run_code(data: dict, api_key: str = Depends(verify_api_key)):
#     # Your code logic here
#     input_data = data.get("input")
#     # Example: process input_data and generate output
#     output = query(input_data)
#     return {"status": "success", "output": output}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}
