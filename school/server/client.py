import socketio
import asyncio

sio = socketio.AsyncClient()

@sio.event
async def connect():
    print("Connected to server.")

@sio.event
async def disconnect():
    print("Disconnected from server.")

async def main():
    await sio.connect("http://127.0.0.1:8000")
      
    
    await sio.wait()

if __name__ == "__main__":
    asyncio.run(main())
