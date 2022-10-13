import time  # for adding a delay to database reconnecting
from multiprocessing import synchronize
from random import randrange  # for generrating random number
from turtle import pos, title
from typing import List, Optional

import psycopg2
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.params import Body
from psycopg2.extras import \
    RealDictCursor  # for returning data as column & row wise data
from pydantic import BaseModel
from sqlalchemy.orm import Session

from . import models, schemas, utils
from .database import engine, get_db
from .routers import auth, post, user

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


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"data": "hello world"}




