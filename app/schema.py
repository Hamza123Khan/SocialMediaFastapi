from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    # create_at: datetime
    
    class Config:
        orm_mode = True
class create_users(BaseModel):
    username: str
    email: EmailStr
    password: str

class userout(BaseModel):
    id:int
    username:str
    email:EmailStr

    class config:
        orm_mode=True

class login(BaseModel):
    username: str
    email: EmailStr
    password: str

class tokken(BaseModel):
    accesstokken: str
    tokkentype: str

class Tokkendata(BaseModel):
    id: Optional[str] = None