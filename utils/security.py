from passlib.context import CryptContext
from model.jwt_user import JWTUser
from utils.const import JWT_ALGORITHM, JWT_EXPIRATION_IN_MINUTS, JWT_SECRET_KEY
from datetime import datetime, timedelta
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import time
from starlette.status import HTTP_401_UNAUTHORIZED

pwd_context = CryptContext(schemes=["bcrypt"])
outh_schema = OAuth2PasswordBearer(tokenUrl="/token")

jwt_user1 = {
    "username": "user1",
    "password": "$2b$12$DQ/wv6assPzArc3zGoNtZOBgGMm2KZPmVBJEgrAuyW6/hm9lYN8Rq",
    "disabled": False,
    "role": "admin"
}

fake_jwt_user1 = JWTUser(**jwt_user1)


def get_hashed_password(password):
    '''
    :param password:
    :return: hashed password
    '''
    return pwd_context.hash(password)

def verify_password(password, hashed_pass):
    '''
    :param password:
    :param hashed_pass:
    :return: True or False based on both params matching
    '''
    try:
        return pwd_context.verify(password, hashed_pass)
    except Exception as e:
        return False

# function to check if username & password given to jwt_token
def authenticate_user(user : JWTUser):
    if fake_jwt_user1.username == user.username:
        if verify_password(user.password, fake_jwt_user1.password):
            user.role = "admin"
            return user
    return None


def create_jwt_token(user: JWTUser):
    expiration = datetime.utcnow() + timedelta(minutes= JWT_EXPIRATION_IN_MINUTS)
    jwt_payload = {
        "sub": user.username,
        "role": user.role,
        "exp":  expiration
    }

    jwt_token = jwt.encode(jwt_payload, algorithm=JWT_ALGORITHM, key=JWT_SECRET_KEY)
    return jwt_token

# check is jwt token is correct :
def check_jwt_token(token : str= Depends(outh_schema)):
    try:
        jwt_payload = jwt.decode(token,key=JWT_SECRET_KEY,algorithms=JWT_ALGORITHM)
        username = jwt_payload.get("sub")
        role = jwt_payload.get("role")
        expiration = jwt_payload.get("exp")
        if time.time() < expiration:
            if fake_jwt_user1.username == username:
                return final_check(role)
    except Exception as e:
        raise False
    raise False


def final_check(role : str):
    if role == "admin":
        return True
    raise False

