from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

# Pydantic schema for User Body validation (REQUEST)
class User(BaseModel):
    email: EmailStr  # str is too general (random text)
    password: str


# Pydantic shchema for /auth body validation (REQUEST)
class User_Credentials(User):
    pass #pass means we want the same fields like User


# Pydantic schema User Response (RESPONSE)
class User_Response(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:  # Important for pydantic model/schema translation
        orm_mode = True


# Pydantic schema for POST REQUEST Body validation (REQUEST)
class BlogPost(BaseModel):  
    title: str
    content: str
    author: str
    rating: Optional[int] = None
    published: bool = True


# Pydantic schema for POST REQUEST Body validation (RESPONSE)
class BlogPost_Response(BlogPost):  
    id: int
    created_at: datetime
    writer: User_Response
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token : str
    token_type: str
