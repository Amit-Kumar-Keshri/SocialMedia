from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

#schema / pydantic model
#input from the user

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
    
class PostCreate(PostBase): # inherit from PostBase class
    pass

#response to the user
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    
    class Config:
        orm_mode = True

#input from the user
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    

#response to the user
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True
        
# users loging data
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    class Config:
        orm_mode = True
        
# creating token for jwt token  
class Token(BaseModel):
    access_token: str
    token_type: str
    
    
# data embeded to access token
class TokenData(BaseModel):
    id: Optional[str] = None
    
