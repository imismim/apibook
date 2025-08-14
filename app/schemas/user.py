from pydantic import BaseModel
from enum import Enum

class RoleEnum(str, Enum):
    reader = "reader"
    writer = "writer"
    admin = "admin"

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    role: RoleEnum = RoleEnum.reader

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(UserBase):
    id: int
    role: RoleEnum

    class Config:
        from_attributes = True
