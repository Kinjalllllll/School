from fastapi import Depends,HTTPException,status
from jose import jwt
from fastapi.security import OAuth2PasswordBearer

from auth_token import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")


def get_current_user(token: str =  Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_data = verify_token(token, credentials_exception)
    return user_data