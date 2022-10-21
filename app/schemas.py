from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, conint

#schema / pydantic model
#input from the user

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
    
class PostCreate(PostBase): # inherit from PostBase class
    pass

#response to the user
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
        
#response to the user and also inherit from PostBase
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut  # for returning the data of user from pydantic model UserOut
    
    class Config:
        orm_mode = True
        
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

#input from the user
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    



        
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
    
    
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)   # it will take as parameter is 0 & 1 
