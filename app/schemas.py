from pydantic import BaseModel


#schema / pydantic model

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase): # inherit from PostBase class
    pass



