from fastapi import APIRouter, Depends, status, HTTPException
from app.database import db
from .. import schemas, models, utils, security
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])


@router.post('/login', response_model=schemas.Token)
def login(db: db, user_credentials: OAuth2PasswordRequestForm = Depends()):
    
    # OAuth2PasswordRequestForm takes the credential as username, although it is actually the email
    user = db.query(models.User.email==user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # create a token
    access_token = security.create_access_token(data = {"user_id": user.id})
    # return token
    return {"access_token": access_token, "token_type": "bearer"}


    
    

    