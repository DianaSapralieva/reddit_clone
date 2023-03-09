from fastapi import Depends, Response, status, HTTPException, APIRouter
from typing import List
from .. import models, schemas #. means current folder
from ..database import get_db  #. means current folder
from sqlalchemy.orm import Session
from ..utilities import hash_manager, jwt_manager
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix="/webs",
    tags= ["Web"]
    )


# GET All the links between BlogPosts and Websites (ie: BlogPosts published on which websites)
@router.get('/', response_model=List[schemas.Link2_Response])
def get_blog_web(db: Session = Depends(get_db), 
                 user_id: int = Depends(jwt_manager.decode_token)):
    all = db.query(models.Link).all()
    return all


# CREATE an new BLogPost and publish/link it with a new Website
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.New_Website_Response)
def create_posts_web(new_web: schemas.New_Website_Request ,db: Session = Depends(get_db), user_id: int = Depends(jwt_manager.decode_token)):
    
    # Create new Blogpost
    new_blog = models.BlogPost(title = new_web.title, content = new_web.content, author = new_web.author, rating = new_web.rating,
                               published = new_web.published, writer_id = user_id) 
    db.add(new_blog)
    db.flush()
    db.refresh(new_blog)
    blog_id = new_blog.id
    
    # Create new Website
    new_website = models.Website(name = new_web.name, url = new_web.url)
    db.add(new_website)
    db.flush()
    db.refresh(new_website)
    web_id = new_website.id
    
    # Create new Link (ie. publish new blogpost to the new website)
    new_link = models.Link(post_id=blog_id, web_id=web_id)
    db.add(new_link)
    db.commit()  # Save the modification to the DB
    db.refresh(new_link)

    # Prepare the response by using the pydantic schema
    response_body = schemas.New_Website_Response(title = new_web.title, content = new_web.content, author = new_web.author, rating = new_web.rating,
                               published = new_web.published, name = new_web.name, url = new_web.url)
    return response_body