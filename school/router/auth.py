from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
import schema,model,auth_token
import database
from hashing import Hash
from passlib.context import CryptContext
from auth_token import create_access_token
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")  

@router.post('/login',tags=['user'])
def login(request:OAuth2PasswordRequestForm = Depends(), db : Session = Depends(database.get_db)):
    user = db.query(model.User).filter(model.User.name == request.username).first()
    print("user", user)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid credentials")
    
    if not Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")
    
    access_token = create_access_token(data={"sub": request.username})
    return {"access_token":access_token, "token_type":"bearer"}



    
