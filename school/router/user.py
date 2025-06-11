
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
import model,schema,hashing
from schema import EmailSchema
import database,oauth2
from typing import List
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from typing import List
from starlette.responses import JSONResponse
from .user_service import conf


from router.user_service import send_email

router = APIRouter()
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")




@router.post("/user", tags=['user'])
def create_user(request: schema.User,db: Session = Depends(database.get_db),current_user: schema.User = Depends(oauth2.get_current_user)):
    hashedPassword = pwd_cxt.hash(request.password)
    new_user = model.User(name=request.name,email=request.email,password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/user/', response_model=schema.User, tags=['user'])
def get_current_user(db: Session = Depends(database.get_db), token_data: schema.TokenData = Depends(oauth2.get_current_user)):
    user = db.query(model.User).filter(model.User.name == token_data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get('/user/', response_model=List[schema.User], tags=['user'])
def get_all_user(db: Session = Depends(database.get_db),current_user: schema.User = Depends(oauth2.get_current_user)
):
    user = db.query(model.User).all()
    return user


@router.put('/user/{user_id}',tags=['user'])
def update_user(user_id: int, user_update: schema.UserUpdate, db: Session = Depends(database.get_db)):
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user_update.model_dump(exclude_unset=True)

    # if "password" in update_data:
    #     update_data["password"] = hash.password(update_data["password"])
    # for key, value in update_data.items():
    #     setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


@router.delete('/user/{user_id}',tags=['user'])
def destroy(user_id: int,db:Session = Depends(database.get_db),current_user: schema.User = Depends(oauth2.get_current_user)):
    db.query(model.User).filter(model.User.id == user_id).delete(synchronize_session=False)
    db.commit()
    return {"message": "User deleted successfully"}




@router.post("/email",tags=['user'])
async def simple_send(email: EmailSchema) -> JSONResponse:

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"),
       
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"}) 
