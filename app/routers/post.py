
from typing import Optional
from .. import oauth2
from .. import models, schema
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db
# from ..oauth2 import oaut

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/sqlalchemy")
def testpost(db: Session = Depends(get_db)):
    test_db = db.query(models.POST).all()
    return {"status": test_db}


@router.get("/", response_model=list[schema.Post])
def get_posts(db: Session = Depends(get_db), currentuser: int =  Depends(oauth2.getcurrentuser),
               limitposts : int = 10, search: Optional[str] = ""):

    test_db = db.query(models.POST).filter(models.POST.title.contains(search)).limit(limitposts).all()
    return test_db

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_post(post: schema.PostCreate, db: Session = Depends(get_db), currentuser: int =  Depends(oauth2.getcurrentuser)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """,(post.title, post.content, post.published))
    # new_post_1 = cursor.fetchone()
    # conn.commit()
    print(currentuser.email)
    new_post_1 = models.POST(user_id = currentuser.id, **post.dict())
    db.add(new_post_1)
    db.commit()
    db.refresh(new_post_1)

    return new_post_1


@router.get("/{id}", response_model=schema.Post)
def get_post(id: int, db: Session = Depends(get_db), currentuser: int =  Depends(oauth2.getcurrentuser)):
    post = db.query(models.POST).filter(models.POST.id == id).first()
    

    # cursor.execute("""SELECT * from posts WHERE id = %s """,(str(id)))
    # post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id not founded {id}")
    if post.user_id != currentuser.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"the user is unauthenticated ")
    return  post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), currentuser: int =  Depends(oauth2.getcurrentuser)):
    DELETEDPOST = db.query(models.POST).filter(models.POST.id == id)
    poste = DELETEDPOST.first()
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,(str(id),))
    # DELETEDPOST = cursor.fetchone()
    # conn.commit()
    if poste == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id not foounded {id}")
    
    if poste.user_id != currentuser.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"the user is unauthenticated ")
    
    DELETEDPOST.delete(synchronize_session=False)
    db.commit()

    return "post successfully deleted"

@router.put("/{id}", response_model=schema.Post)
def update_post(id: int, post: schema.PostCreate, db: Session = Depends(get_db), currentuser: int =  Depends(oauth2.getcurrentuser)):
    # cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING 
    #                *""",(post.title, post.content, post.published,str(id)))
    # updaePOST = cursor.fetchone()
    # conn.commit()
    updaePOST = db.query(models.POST).filter(models.POST.id == id)
    post1 = updaePOST.first()

    if post1 == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id not foounded {id}")
    
    if post1.user_id != currentuser.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"the user is unauthenticated ")

    updaePOST.update(post.dict(),synchronize_session=False)
    db.commit()
    return updaePOST.first( )
