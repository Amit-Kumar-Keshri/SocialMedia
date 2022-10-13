
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, models, oauth2, schemas, utils

router = APIRouter(tags=['Authentication'])

#OAuth2PasswordRequestForm - this form only argument takes is "username" and "password" only here.
# verfying users login credentials
@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session= Depends(database.get_db)):
    
    """
     here in user_credentials we get here only username and password like
    {
        "username": "",
        "password": ""
    } like this we cant use email here
    """
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    # create a token 
    # return token
    
    access_token = oauth2.create_access_token(data={"user_id": user.id}) # in parameter we are passing only id here to jwt tokens payload, if we to provide anything else we can also provide that
    
    return {"access_token": access_token, "token_type": "bearer"} # we only return the token here and the token type is bearer here


