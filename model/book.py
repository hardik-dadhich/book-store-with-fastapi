from pydantic import BaseModel
from model.author import Author

class Book(BaseModel):
    name: str
    isbn: str
    author: Author
    year: int
