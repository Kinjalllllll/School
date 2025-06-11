from fastapi import FastAPI
import model
import database
from router import auth
from router import user
from router import stud
import server.chat as chat
from fastapi_pagination import Page, add_pagination, paginate



app = FastAPI()
add_pagination(app)


model.Base.metadata.create_all(bind=database.engine)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(stud.router)

# app.include_router(chat.router)
