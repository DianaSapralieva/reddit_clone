from jose import jwt, JWTError
from ..schemas import Token
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta

# Instantiate Oauth2 feature forward consumer to the /auth endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

# openssl rand -hex 32
SERVER_KEY = "f0ab9be43c7962b1f1ed157554fe701c307f18086d6292a4b2fa1835140fa23f"
ALGORITHM = "HS256"
EXPIRATION_MINUTES = 30 # token expiration time 30 minutes

# Function generate token
def generate_token(id: int):
    payload = {"user_id": id}
    payload.update({"exp": datetime.utcnow() + timedelta(minutes=EXPIRATION_MINUTES)})
    encoded_jwt = jwt.encode(payload, SERVER_KEY, algorithm=ALGORITHM)
    return Token(access_token=encoded_jwt, token_type="bearer")

# Function to decode the token
def decode_token(provided_token = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(provided_token, SERVER_KEY, algorithms=[ALGORITHM])
        decoded_id = payload.get("user_id")
    except JWTError:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail = "Could not validate Token",
            headers={"WWW-Authenticate":"Bearer"}
        )
    return decoded_id