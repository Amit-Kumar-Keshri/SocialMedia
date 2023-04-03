from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from . import database, models, schemas
from .config import settings

oauth_scheme = OAuth2PasswordBearer(tokenUrl= 'login')

# Secret_key
# algo 
# Expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes



# creating jwt tokens
def create_access_token(data: dict):
    to_encode = data.copy() # to manipulate data i had made a copy of data so that data will not manipulate into the database
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})  # this is Expiration time which we pass to jwt that after how time it get expire
    
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)  # created jwt tokens
    
    return encode_jwt

# verifying access token
def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # payload consists of of tokens, SECRET_KEY, algorithm

        id: str = payload.get("user_id") # extracting id from token
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
     
    return token_data
    

def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(database.get_db)):
    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id==token.id).first()
    
    return user