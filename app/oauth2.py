from jose import jwt, JWTError
from datetime import datetime, timedelta
from . import schema
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

OAuthschema = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def createtokken (data: dict):
    toencode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    toencode.update({"exp":expire})
    encodedjwt = jwt.encode(toencode, SECRET_KEY, algorithm=ALGORITHM)
    return encodedjwt


def verifyaccesstokken (tokken: str, credentials_execption):
    
    try:
        print(tokken)
        payload = jwt.decode(tokken, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("userid")
        if id is None:
            raise credentials_execption
        tokendata = schema.Tokkendata(id=str(id))
    except JWTError as e:
        print(e)
        raise credentials_execption
    except AssertionError as e:
        print(e)
    
    return tokendata
    
def getcurrentuser(tokken: str = Depends(OAuthschema)):
    credentials_execption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"cloud not found the individuals",
                                           headers={"www-Authenticate": "Bearer"})
    return verifyaccesstokken(tokken, credentials_execption)

