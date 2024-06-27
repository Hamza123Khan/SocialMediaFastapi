from jose import jwt, JWTError
from datetime import datetime, timedelta
from . import schema, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .config import settings

OAuthschema = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_tokken_expire_minutes


def createtokken (data: dict):
    toencode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    toencode.update({"exp":expire})
    encodedjwt = jwt.encode(toencode, SECRET_KEY, algorithm=ALGORITHM)
    return encodedjwt


def verifyaccesstokken (tokken: str, credentials_execption):
    
    try:
        payload = jwt.decode(tokken, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("userid")
        if id is None:
            raise credentials_execption
        tokendata = schema.Tokkendata(id=str(id))
    except JWTError as e:
        print(e)
        raise credentials_execption
    
    return tokendata
    
def getcurrentuser(tokken: str = Depends(OAuthschema), db: Session = Depends(get_db)):
    credentials_execption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"cloud not found the individuals",
                                           headers={"www-Authenticate": "Bearer"})
    token = verifyaccesstokken(tokken, credentials_execption)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    print(user)
    return user

