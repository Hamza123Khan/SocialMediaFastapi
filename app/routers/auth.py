from .. import models, schema, utils, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import engine, get_db


router = APIRouter(
    tags=['Authentication']
)


@router.post('/login')
def login(user_cred: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    emailusr = db.query(models.User).filter(models.User.email == user_cred.username).first()
    if not emailusr:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid credentails")
    if not utils.verify(user_cred.password, emailusr.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalis cred")
    
    access_tokken = oauth2.createtokken(data={"userid": emailusr.id})
    return {"access_tokken": access_tokken, "tokentype":"bearer"}