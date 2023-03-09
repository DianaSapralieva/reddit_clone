from fastapi import Depends, Response, status, HTTPException, APIRouter
from .. import models, schemas #. means current folder
from ..database import get_db  #. means current folder
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..utilities import jwt_manager

router = APIRouter(
    prefix="/posts",
    tags= ["Posts"]
)

############### BLOGPOSTS ENDPOINTS ####################
# GET ALL BLOGPOSTS
@router.get("/")
def get_posts(db: Session = Depends(get_db), user_id: int = Depends(jwt_manager.decode_token)):
    all_posts = db.query(models.BlogPost).all()
    return {"data": all_posts}

#
# Create new blogpost endpoint
#
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.BlogPost_Response)
def create_posts(post_body: schemas.BlogPost, db: Session = Depends(get_db), user_id: int = Depends(jwt_manager.decode_token)):
    try:
        new_post = models.BlogPost(**post_body.dict(), writer_id = user_id) # ** pass to the model builder from SQLAlchemy the serialize of the pydantic model
        db.add(new_post)  # Execute the INSERT
        db.commit()  # Save the modification to the DB
        db.refresh(new_post)  # to replace "RETURNING *"
        return new_post
    except IntegrityError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail= f"Foreignkey violation with writer_id:{post_body.writer_id} \n\n ****ERR*****: {err}")

#
# get blogpost with ID
#
@router.get('/{uri_id}', response_model=schemas.BlogPost_Response)
def get_post(uri_id: int, db: Session = Depends(get_db), user_id: int = Depends(jwt_manager.decode_token)):
    corresponding_post = db.query(models.BlogPost).filter(
        models.BlogPost.id == uri_id).first()
    if not corresponding_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not corresponding post was found with id:{uri_id}"
        )
    return corresponding_post

#
# DELETE blogpost endpoint
#
@router.delete('/{uri_id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(uri_id: int, db: Session = Depends(get_db), user_id: int = Depends(jwt_manager.decode_token)):
    # find blogpost with id provided            
    query_post = db.query(models.BlogPost).filter(models.BlogPost.id == uri_id)
    corresponding_post = query_post.first()
    # Check if this post exists
    if not corresponding_post:  
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not corresponding post was found with id:{uri_id}"
        )
    # Check if the writer_id correspond to the user_id
    if corresponding_post.writer_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized deleting what you haven't writen"
        ) 
    query_post.delete()  # DELETE the post
    db.commit()  # Save changes to the DB
    return Response(status_code=status.HTTP_204_NO_CONTENT)       

#
# UPDATE blogpost endpoint
#
@router.put('/{uri_id}', response_model=schemas.BlogPost_Response)
def update_post(uri_id: int, post_body: schemas.BlogPost, db: Session = Depends(get_db), user_id: int = Depends(jwt_manager.decode_token)):
    try:
        # find blogpost with id provided                
        query_post = db.query(models.BlogPost).filter(models.BlogPost.id == uri_id)
        corresponding_post = query_post.first()
        if not corresponding_post:  # make sure it exists
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Not corresponding post was found with id:{uri_id}"
            )
        # Check if the writer_id correspond to the user_id
        if corresponding_post.writer_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized updating what you haven't writen"
            ) 
        query_post.update(post_body.dict())  # Update the posts
        db.commit()  # Save changes to DB
        return query_post.first()
    except IntegrityError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail= f"Foreignkey violation with writer_id:{post_body.writer_id} \n\n ****ERR*****: {err}")