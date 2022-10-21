
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


# creating some database models of posts
class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default='TRUE', nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable= False)
    
    owner = relationship("User") # this code does is fetch the user data from User class 

# creating some database models of users    
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, nullable=False, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=text('now()'))
    
    
# creating some database models of votes
class Vote(Base):
    __tablename__ = "votes"
    
    post_id = Column(Integer,  ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer,  ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
