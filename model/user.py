from pydantic import BaseModel
import enum

class Role(enum.Enum):
    admin = "admin"
    person = "person"

class User(BaseModel):
    name: str
    password: str
    email: str
    role: Role

