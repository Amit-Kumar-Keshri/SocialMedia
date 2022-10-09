from datetime import datetime
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
