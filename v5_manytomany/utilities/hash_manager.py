from passlib.context import CryptContext

# Initialize teh CryptoContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pass(password: str):
    return pwd_context.hash(password) #hashed password

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password) # if passwords are matching