from fastapi import FastAPI, Body, HTTPException, Header, Depends, APIRouter
from model.user import User
from model.book import Book
from model.author import Author
from utils.security import *
from model.jwt_user import JWTUser
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_201_CREATED
from fastapi.security import OAuth2PasswordRequestForm
import time

app_v1 = APIRouter()


@app_v1.post("/user", status_code=HTTP_201_CREATED)
async def post_user(user: User):
    return {"Body ": user}

# query params pass like /user?password
@app_v1.get("/user")
async def get_user_validation(password: str):
    return {"query parameters": password}

# query param like varible ex : /book/isbn1
# response_model is for customising the response you get as a result
# we can pass more same customisation like "respose_model_exclude" and "response_model_include"
@app_v1.get("/book/{isbn}", response_model=Book)
async def get_book_with_isbn(isbn: str):
    author_dict = {
        "name": "name1",
        "book": ["book1", "book2"]
    }
    author1 = Author(**author_dict)

    book_dict = {
        "name": "mr kishan",
        "isbn": "124",
        "author": author1,
        "year": 1292
    }
    book1 = Book(**book_dict)
    return book1
    #return {"Book isbn": isbn}

# param like variable +  query param ex /author/123/book?catagory="novel"
@app_v1.post("/author/{id}/book")
async def get_authors_books(id: int, catagory: str, order: str = "asc"):
    return {"the return params ": order + catagory + str(id)}

# when we have to patch json body , NOTE : "..." says its required and embed is for restricting Keys
@app_v1.patch("/author/name")
async def patch_author_name(name: str = Body(..., embed=True)):
    return {"name in body ": name}


@app_v1.post("/user/author")
async def post_user_and_author(user: User, author: Author, bookstore_name: str = Body(..., embed=True)):
    return {
    "user is ": user,
    "author is ": author,
    "bookstore name " : bookstore_name
    }


@app_v1.post("/token", description="It checks the username and password and returns the JWT token to you", summary="Return the JWT token")
async def login_for_access_token(form_data : OAuth2PasswordRequestForm = Depends()):
    jwt_user_dict = {
        "username": form_data.username,
        "password": form_data.password
    }
    jwt_user = JWTUser(**jwt_user_dict)
    user = authenticate_user(jwt_user)

    if user is None:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
    jwt_token = create_jwt_token(user)
    return {"access_token ": jwt_token}