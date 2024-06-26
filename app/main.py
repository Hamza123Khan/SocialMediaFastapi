from fastapi import FastAPI 
from . import models
from .database import engine
from .routers import post, users, auth, votes
from .config import settings
print(settings.database_username)


models.base.metadata.create_all(bind=engine)
    

app = FastAPI()

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)
