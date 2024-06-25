from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor  
from . import models, schema, utils
from sqlalchemy.orm import Session
from .database import engine, get_db
from .routers import post, users, auth


models.base.metadata.create_all(bind=engine)



try:
    conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='123', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("sucessful database connection")
except Exception as error:
    print("connection is not made",error)
    

        # rating: Optional[int] = None
app = FastAPI()

my_posts = [{"title": "title of post 1", "content":"content of post 1", "id":1},
            {"title": "title of post 2", "content":"content of post 2", "id":2}]


# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p
        
# def find_theindex(id):
#     for i,p in enumerate(my_posts):
#         if p['id'] == id:
#             return i




app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)



# @app.get("/login")
# def root():
#     return {"message":"helloworld"}