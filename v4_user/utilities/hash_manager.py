from passlib.context import CryptContext

# Intilialize the CryptoContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash a plain text password
def hash_pass(password: str):
    return pwd_context.hash(password)#hashed password

# Function to verify plain text password with hashed password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)# if passwords are matching