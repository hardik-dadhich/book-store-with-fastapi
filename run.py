from fastapi import FastAPI
from routs.v1 import app_v1
from routs.v2 import app_v2
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED
from datetime import datetime


# this is for Versioning your APIs
# We divided our verson into 2 routs
app = FastAPI()
app.mount("/v1", app_v1)
app.mount("/v2", app_v2)


# A middleware which is to moidfy request and response
@app.middleware("http")
async def middleware(request: Request, call_next):
    start_time = datetime.utcnow()
    # modifying request
    if not str(request.url).__contains__("/token"):
        try:
            jwt_token = request.headers["Authorization"].split("Bearer ")[1]
            is_valid = check_jwt_token(jwt_token)
        except Exception as e:
            is_valid = False
        if not is_valid:
            return Response("unauthprized", status_code=HTTP_401_UNAUTHORIZED)

    response = await call_next(request)

    # modify response
    execution_time = datetime.utcnow() - start_time
    response.headers["x-execution-time"] = str(execution_time)
    return response




