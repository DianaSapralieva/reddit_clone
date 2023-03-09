from fastapi import Depends, status, HTTPException, APIRouter
from .. import models, schemas 
from ..database import  get_db
from sqlalchemy.orm import Session
from ..utilities import hash_manager, jwt_manager
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

incorrect_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate":"Bearer"}
        )  
#
# /Auth Consumer Endpoint
#
@router.post('/', response_model=schemas.Token )
def auth_user(user_credentials: OAuth2PasswordRequestForm = Depends(),
              db: Session = Depends(get_db)):
     #get corresponding user from database   
     corresponding_user = db.query(models.User).filter(models.User.email == user_credentials.username).first()      
     #if not corresponding user found, raise an exception
     if not corresponding_user:
        raise incorrect_exception 
     #Check the password
     pass_valid = hash_manager.verify_password(user_credentials.password, 
                                               corresponding_user.password)  
     #if password invalid, raise an exception
     if not pass_valid:
        raise incorrect_exception
     #generate the token
     jwt = jwt_manager.generate_token(corresponding_user.id)    
     return jwt #return the generated token