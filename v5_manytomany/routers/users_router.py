from fastapi import Depends, Response, status, HTTPException, APIRouter
from typing import List
from .. import models, schemas #. means current folder
from ..database import get_db  #. means current folder
from sqlalchemy.orm import Session
from ..utilities import hash_manager, jwt_manager


router = APIRouter(
    prefix="/users",
    tags= ["Users"]
)

############### USERS ENDPOINTS ####################
#
# GET all the users endpoint
#
@router.get('/', response_model=List[schemas.User_Response])
def get_users(db: Session = Depends(get_db), user_id: int = Depends(jwt_manager.decode_token)):
    all_users = db.query(models.User).all()
    return all_users

#
# GET user from ID endpoint
#
@router.get('/{uri_id}', response_model=schemas.User_Response)
def get_user(uri_id:int, db:Session=Depends(get_db), user_id: int = Depends(jwt_manager.decode_token)):
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
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.User_Response)
def create_user(user_body: schemas.User, db: Session = Depends(get_db)):
    # Hashing the password
    pwd_hashed = hash_manager.hash_pass(user_body.password)
    user_body.password = pwd_hashed # Overwrite password in body by hashed password
    new_user = models.User(**user_body.dict()) #** pass to the model builder from SQLAlchemy the serialize of the pydantic model
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#
# DELETE USER
#
@router.delete('/{uri_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(uri_id: int, db: Session = Depends(get_db), user_id: int = Depends(jwt_manager.decode_token)):
    # find user with id provided             
    query_user = db.query(models.User).filter(
        models.User.id == uri_id)
    if not query_user.first():  # Check if user exists
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No corresponding user was found with id:{uri_id}"
        )
    query_user.delete()  # DELETE the user
    db.commit()  # Save changes to the DB
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#
# UPDATE USERS endpoint
#
@router.put('/{uri_id}', response_model=schemas.User_Response)
def update_user(uri_id: int, user_body: schemas.User, db: Session = Depends(get_db),user_id: int = Depends(jwt_manager.decode_token)):
    # find user with id provided                
    query_user = db.query(models.User).filter(models.User.id == uri_id)
    if not query_user.first():  # make sure it exists
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No corresponding user was found with id:{uri_id}"
        )
    query_user.update(user_body.dict())  # Update the user
    db.commit()  # Save changes to DB
    return query_user.first()