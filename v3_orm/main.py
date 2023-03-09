from fastapi import Depends, FastAPI, Body, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from . import models, schemas #. means current folder
from .database import database_engine, get_db  #. means current folder
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

#Create the tables if they don't exist yet
models.Base.metadata.create_all(bind=database_engine)
    
# Pydantic schema for POST Body (sent by Client) validation
class BlogPost(BaseModel):
    title: str
    content: str
    author: str
    rating: Optional[int] = None
    published: bool = True

# API instance name
app = FastAPI()

########################################################
#########               ENDPOINTS               ########
########################################################


############### BLOGPOSTS ENDPOINTS ####################
# GET ALL BLOGPOSTS
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    all_posts = db.query(models.BlogPost).all()
    return {"dataposts": all_posts}


#
# Create new blogpost endpoint
#
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.BlogPost_Response)
def create_posts(post_body: schemas.BlogPost, db: Session = Depends(get_db)):
    try:
        new_post = models.BlogPost(**post_body.dict()) # ** pass to the model builder from SQLAlchemy the serialize of the pyydantic model
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
@app.get('/posts/{uri_id}', response_model=schemas.BlogPost_Response)
def get_post(uri_id: int, db: Session = Depends(get_db)):
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
@app.delete('/posts/{uri_id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(uri_id: int, db: Session = Depends(get_db)):
    # find blogpost with id provided             
    query_post = db.query(models.BlogPost).filter(
        models.BlogPost.id == uri_id)
    if not query_post.first():  # Check if this post exists
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not corresponding post was found with id:{uri_id}"
        )
    query_post.delete()  # DELETE the post
    db.commit()  # Save changes to the DB
    return Response(status_code=status.HTTP_204_NO_CONTENT)



#
# UPDATE blogpost endpoint
#
@app.put('/posts/{uri_id}', response_model=schemas.BlogPost_Response)
def update_post(uri_id: int, post_body: schemas.BlogPost, db: Session = Depends(get_db)):
    try:
        # find blogpost with id provided                
        query_post = db.query(models.BlogPost).filter(models.BlogPost.id == uri_id)
        if not query_post.first():  # make sure it exists
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Not corresponding post was found with id:{uri_id}"
            )
        query_post.update(post_body.dict())  # Update the posts
        db.commit()  # Save changes to DB
        return query_post.first()
    except IntegrityError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail= f"Foreignkey violation with writer_id:{post_body.writer_id} \n\n ****ERR*****: {err}")



############### USERS ENDPOINTS ####################
#
# GET all the users endpoint
#
@app.get('/users', response_model=List[schemas.User_Response])
def get_users(db: Session = Depends(get_db)):
    all_users = db.query(models.User).all()
    return all_users



#
# GET user from ID endpoint
#
@app.get('/users/{uri_id}', response_model=schemas.User_Response)
def get_user(uri_id:int, db:Session=Depends(get_db)):
    corresponding_user = db.query(models.User).filter(models.User.id == uri_id).first()
    if not corresponding_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not user found with the id:{uri_id}"
        )
    return corresponding_user



#
# Create new user
#
@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.User_Response)
def create_user(user_body: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(**user_body.dict()) #** pass to the model builder from SQLAlchemy the serialize of the pydantic model
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


#
# DELETE USER
#
@app.delete('/users/{uri_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(uri_id: int, db: Session = Depends(get_db)):
    # find user with id provided             
    query_user = db.query(models.User).filter(
        models.User.id == uri_id)
    if not query_user.first():  # Check if user exists
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not corresponding user was found with id:{uri_id}"
        )
    query_user.delete()  # DELETE the user
    db.commit()  # Save changes to the DB
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#
# UPDATE USERS endpoint
#
@app.put('/users/{uri_id}', response_model=schemas.User_Response)
def update_user(uri_id: int, user_body: schemas.User, db: Session = Depends(get_db)):
    # find user with id provided                
    query_user = db.query(models.User).filter(models.User.id == uri_id)
    if not query_user.first():  # make sure it exists
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not corresponding user was found with id:{uri_id}"
        )
    query_user.update(user_body.dict())  # Update the user
    db.commit()  # Save changes to DB
    return query_user.first()
