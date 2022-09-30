from sqlite3 import Cursor
from tkinter import CURRENT
from turtle import pos
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange # for generrating random number
import psycopg2
from psycopg2.extras import RealDictCursor  # for returning data as column & row wise data 
import time  # for adding a delay to database reconnecting


app = FastAPI() # created a app


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


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


@app.get("/post")
def get_post():
    cursor.execute("""SELECT * FROM posts""") # for executing the view query
    # cursor.execute("INSERT INTO posts (title, content) VALUES (%s, %s)")
    posts = cursor.fetchall() # for fetch data of all column & row from database
    return {"Data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published)) # for taking input from user in postman or site
    # post_dict = post.dict()
    # post_dict ['id'] = randrange(0,1000000)
    # my_posts.append(post_dict)
    new_post = cursor.fetchone() # for fetch data of one column from database
    conn.commit() # for pushing data to database
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(""" SELECT * FROM posts  WHERE id = %s  """, (str(id)))  # if not work put comma after str typecasting
    post = cursor.fetchone()
    
    # post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    delete_post = cursor.fetchone()
    # index = find_post(id)
    conn.commit()
    
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")


    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
        
    # index = find_post(id)
    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    # post_dict = post.dict()
    # post_dict["id"] = id
    # my_posts[index] = post_dict
    return {"Message": updated_post}
