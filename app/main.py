from multiprocessing import synchronize
from turtle import pos, title
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel

from random import randrange # for generrating random number
import psycopg2
from psycopg2.extras import RealDictCursor  # for returning data as column & row wise data 
import time  # for adding a delay to database reconnecting
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db





models.Base.metadata.create_all(bind=engine)

app = FastAPI() # created a app




while True:
    try:
        # for proding rquired info to connect with database
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password='king1299', cursor_factory=RealDictCursor)
        cursor = conn.cursor() # connecting database
        print("Database connection was succesfully!")
        break
    except Exception as error:
        print("Connecting to database failed!")
        print("Error: ", error)
        time.sleep(2) # added 2 sec dealy for reconnecting database


my_posts = [{"title": "title of post1", "content": "content of post 1", "id": 1}, {
    "title": "favorite foods", "content": "I like Gaming", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
async def root():
    return {"data": "hello world"}


@app.get("/post", response_model=List[schemas.Post])
def get_post(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""") # for executing the view query
    # # cursor.execute("INSERT INTO posts (title, content) VALUES (%s, %s)")
    # posts = cursor.fetchall() # for fetch data of all column & row from database
    posts = db.query(models.Post).all()
    return  posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published)) # for taking input from user in postman or site
    # # post_dict = post.dict() // 1st hardcoded
    # # post_dict ['id'] = randrange(0,1000000)
    # # my_posts.append(post_dict)
    # new_post = cursor.fetchone() # for fetch data of one column from database
    # conn.commit() # for pushing data to database
    
    # new_post = models.Post(title=post.title,content = post.content, published = post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts  WHERE id = %s  """, (str(id)))  # if not work put comma after str typecasting
    # post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND // 1st hardcoded
        # return {"message": f"post with id: {id} was not found"}
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # # index = find_post(id) // 1st hardcoded
    # conn.commit()
    
    post = db.query(models.Post).filter(models.Post.id == id)
    
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post.delete(synchronize_session= False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostBase , db: Session = Depends(get_db)):
    
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id==id)
        
    # index = find_post(id) // 1st hardcoded
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
        
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    # post_dict = post.dict()// 1st hardcoded
    # post_dict["id"] = id
    # my_posts[index] = post_dict
    return  post_query.first()


#for users
@app.post("/users",status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):
    
    #hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@app.get("/user/{id}")
def get_user(id: int, db: Session =Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with the id : {id} was not found")
    print(user)
    return user