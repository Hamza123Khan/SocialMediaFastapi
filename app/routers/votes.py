from .. import schema, models, oauth2
from . import users, post, auth
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db


router = APIRouter(
    prefix= "/votes",
    tags= ['votes']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def getvotes(vote: schema.Vote, db: Session = Depends(get_db), currentuser: str = Depends(oauth2.getcurrentuser)):



    post = db.query(models.POST).filter(models.POST.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post not founded {vote.post_id} deos not exist")
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == currentuser.id)
    found_vote = vote_query.first()
    
    try:
        if(vote.dir == 1):
            print("helloworld")
            if found_vote:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user  already votes on")        
            newvotes = models.Votes(post_id = vote.post_id, user_id = currentuser.id)
            print("helloworld")
            db.add(newvotes)
            db.commit()
            return {"message": "successflly added votes"}
    except HTTPException as e:
        print (e)
    else: 
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="votes does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "sucessfully deleted vote"}