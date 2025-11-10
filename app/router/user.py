from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from .. import models, schemas, utils

from ..database import db


router = APIRouter(prefix="/users", tags=["Users"])



@router.Post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(db: db, user: schemas.UserCreate):

    """
    Create a new user.

    Args:
        db (db): The database session.
        user (schemas.UserCreate): The user details.

    Returns:
        schemas.UserOut: The created user.
    """

    # hash the password first
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    # get the details of user in a dictionary
    user_data = user.model_dump()

    # create user by passing the details in the constructor
    new_user = models.User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(db: db, id: int):

    
    """
    Retrieve a user by its ID.

    Args:
        db (db): The database session.
        id (int): The user ID.

    Returns:
        schemas.UserOut: The retrieved user.

    Raises:
        HTTPException: If the user with the given ID does not exist.
    """
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"user with id: {id} does not exist")
    return user


    
