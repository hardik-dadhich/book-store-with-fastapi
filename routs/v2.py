from fastapi import FastAPI, Body

app_v2 = FastAPI()

@app_v2.get("/version")
async def get_product_version():
    return {"version is ": int(2.0)}

