
from fastapi import FastAPI

from . import models
from .config import Settings
from .database import engine
from .routers import auth, post, user, vote
from fastapi.middleware.cors import CORSMiddleware

# its tells the sqlalchemy to run the command and genrates the fields in the database when it first started up
# models.Base.metadata.create_all(bind=engine)

app = FastAPI() # created a app

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"data": "hello world"}
