from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional

from sqlalchemy import func

from .. import models, schemas, security
from ..database import db 

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: db, limit:int=10, skip: int = 0, search: Optional[str] = ""):
    """
    Retrieve posts from the database

    Args:
        db (Session): The database session
        limit (int, optional): The maximum number of posts to retrieve. Defaults to 10.
        skip (int, optional): The number of posts to skip. Defaults to 0.
        search (Optional[str], optional): The search query. Defaults to "".

    Returns:
        List[schemas.PostOut]: A list of posts with their vote count
    """
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts






@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(db: db, post: schemas.PostCreate, current_user: int = Depends(security.get_current_user())):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post







@router.get("/{id}", response_model=schemas.PostOut)
def get_post(db: db, id: int, current_user: int = Depends(security.get_current_user)):

    post = db.query(models.Post, func.count(models.Vote.Post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    return post







@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(db: db, id: int, current_user: int = Depends(security.get_current_user())):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)








@router.put("/{id}", response_model=schemas.Post)
def update_post(db: db, id: int, updated_post: schemas.PostCreate, current_user: int = Depends(security.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.update(updated_post.model_dump(), synchronize_session=False)

    db.commit()

    return post_query.first()

