from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    """
    Creates an access token given a dictionary of data.

    The dictionary should contain the necessary information to be
    stored in the token. The token will expire after a certain
    amount of time defined by ACCESS_TOKEN_EXPIRE_MINUTES.

    :param data: The dictionary of data to be stored in the token.
    :return: The encoded JWT token.
    """
    to_encode = data.copy() # we are copying the dictionary so we don't change the original
    
    expire = datetime.now() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt






def verify_access_token(token: str, credentials_exception):
    """
    Verify an access token and return the corresponding user_id.

    :param token: The token to verify.
    :param credentials_exception: The exception to raise if the token is invalid.
    :return: The user_id if the token is valid, otherwise an exception is raised.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credentials_exception

    return token_data




def get_current_user(db: db, token: str = Depends(oauth2_scheme)):
    """
    Return the current user based on the provided token.

    :param db: The database session to use.
    :param token: The token to verify and get the user for.
    :return: The user associated with the token.
    :raises HTTPException: If the token is invalid.
    """
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user



