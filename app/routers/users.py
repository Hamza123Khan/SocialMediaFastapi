from .. import models, schema, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.userout)
def createusers(users: schema.create_users ,db: Session = Depends(get_db)):

    hashespassword = utils.hash(users.password)
    users.password = hashespassword
    new_user = models.User(**users.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}", response_model=schema.userout)
def get_users(id: int, db: Session = Depends(get_db)):
    userss = db.query(models.User).filter(models.User.id == id).first()
    
    if not userss:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no user foundeed by this id {id} ")
    
    return userss





# @router.get("/user/{id}", response_model=schema.PostBase)
# def updateuser(id:int, user = schema.create_users, db:Session=Depends(get_db)):
#     updateuser = db.query(models.User).filter(models.User.id == id).first()
        # if :
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"id not founded{id}")
#     updateuser.update(user.dict(), synchronize_session=False)
#     db.commit()


# @router.get("/user/{id}", response_model=schema.PostBase)
# def updateuser(id:int, user = schema.create_users, db:Session=Depends(get_db)):
#      updateuser = db.query(models.User).filter(models.User.id == id)
#     updateuser.delete(user.dict(), synchronize_session=False)
#     db.commit()











