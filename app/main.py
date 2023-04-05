# from typing import  List
from fastapi import FastAPI
# from fastapi.params import Body
# from random import randrange
from . import models
from .database import engine
from .routers import user, post, auth, vote
from pydantic import BaseSettings
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


# {{URL}}posts?limit=2&skip=1&search=333th%20post

print(settings.database_password)


# #this is what auto creates all the table in postgres..
#we don't have to worry about it again since alembic will be handling our table and migration in postgres


#models.Base.metadata.create_all(bind=engine) 

app = FastAPI()


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




    
# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data": posts}


# my_post is a dictionary acting like a database    
# my_posts = [{"title": "title of post1", "content": "content of post 1", "id": 1},
#             {"title": "favourite foods", "content": "i like pizza", "id": 2}]

# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p["id"] == id:
#             return i



@app.get("/")
def root():

    return {"message": "Hello World"} #return keyword Data sent back to user

# first path operation that matches is going to be run first
# uvicorn main:app --reload


