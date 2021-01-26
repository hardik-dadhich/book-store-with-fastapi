from fastapi import FastAPI, Body, APIRouter

app_v2 = APIRouter()

@app_v2.get("/version")
async def get_product_version():
    return {"version is ": int(2.0)}

