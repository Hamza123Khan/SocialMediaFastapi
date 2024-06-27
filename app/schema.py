from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint




class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # type: ignore

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

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    user_id: int
    user: userout
    # votes: Vote
    # create_at: datetime
    
    class Config:
        orm_mode = True
class create_users(BaseModel):
    username: str
    email: EmailStr
    password: str



class tokken(BaseModel):
    accesstokken: str
    tokkentype: str

class Tokkendata(BaseModel):
    id: Optional[str] = None


