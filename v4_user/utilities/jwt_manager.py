from jose import jwt, JWTError
#import the Token schema
from ..schemas import Token
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from ..config import settings

#Instantiate Oauth2 feature and foward consumer to the /auth endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

# openssl rand -hex 32
SERVER_KEY = settings.database_key
ALGORITHM = settings.algorithm
EXPIRATION_MINUTES = settings.exparation_minutes #token expiration time 30minutes

#function generate token
def generate_token(id: int):
    payload = {"user_id":id}
    payload.update({"exp": datetime.utcnow() + timedelta(minutes=EXPIRATION_MINUTES)})
    encoded_jwt = jwt.encode(payload,SERVER_KEY,algorithm=ALGORITHM)
    return Token(access_token=encoded_jwt, token_type="bearer")

#function to decode the token
def decode_token(provided_token = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(provided_token,SERVER_KEY,algorithms=[ALGORITHM])
        decoded_id = payload.get("user_id")
    except JWTError:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate Token",
            headers={"WWW-Authenticate":"Bearer"}
        )
    return decoded_id