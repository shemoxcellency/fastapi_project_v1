
from typing import  List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import engine, get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)




@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
                 current_user: int = Depends (oauth2.get_current_user), limit: int = 10, skip: int = 0
                 , search: Optional[str] = ""):
    
    # posts= db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    posts= db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(current_user.id)
    # print(posts)
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by\
        (models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(results)
    return results

@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends (oauth2.get_current_user)):
# def create_posts(db: Session = Depends(get_db)):
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0,1c0000000000)
    # print(post.dict()) #convert pydantic model to a dictionary .dict()
    # my_posts.append(post_dict)
    # cursor.execute("""INSERT INTO posts (title, content, published)  VALUES (%s, %s, %s) RETURNING *""", 
    # (post.title, post.content, post.Published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # print(post.dict())
    # print(current_user.id)
    # print(current_user.email)
    new_post = models.Post(user_id = current_user.id, **post.dict()) #unpacking all the pydantic models
    #new_post = models.Post(title=post.title, content = post.content, published = post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# @router.get("/posts/latest")
# def get_latest():
#     post = my_posts[len(my_posts) - 1]
#     return {"detail": post}

# @app.get("/posts/{id}")
# def get_post(id: int, response: Response):
#     post = find_post(id)
#     if not post:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {"message": f"post with id: {id} was not found"}
#     return {"post_detail": post}

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db),
                 current_user: int = Depends (oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts where id = %s """, (str(id),))
    # get_post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by\
        (models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found")
    if post.Post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
        detail="not authorized to perform requested action")
    return post


#Base Model acts a schema that defines what the front end send during the POST requests
# title str, content str, category str, published Bool.... e.t.c

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                 current_user: int = Depends (oauth2.get_current_user)):
    #find the index in the array that has the required ID
    #my_posts.pop(index)
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    # index = find_index_post(id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=
        f"post with id: {id} does not exist")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
        detail="not authorized to perform requested action")
    # my_posts.pop(index)
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends (oauth2.get_current_user)):
    #print(post)
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    # (post.title, post.content, post.Published, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()
    # index = find_index_post(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=
        f"post with id: {id} does not exist")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail="not authorized to perform requested action")
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()