from .sockets import sio_app
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi import FastAPI
import socketio


sio = socketio.AsyncServer(async_mode="asgi")
sio_app = socketio.ASGIApp(sio)  


app = FastAPI()

app.mount('/', app=sio_app)

app.add_middleware(
                    CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                 
)

@app.get("/")
async def home():
    return {"message": "Hello developers"}

if __name__ == "__main__":
    uvicorn.run("server.main:app", host="127.0.0.1", port=8000, reload=True)

# @sio.event
# async def connect(sid, environ):
#     print("Client connected:", sid)

# @sio.event
# async def disconnect(sid):
#     print("Client disconnected:", sid)

# @sio.event
# async def message(sid, data):
#     print("Message received:", data)
#     await sio.emit('message', f"Echo: {data}")

