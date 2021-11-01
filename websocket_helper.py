import asyncio
import websockets
import json

async def get_from_websockets():
  async with websockets.connect(f"ws://aaaa") as websocket:
    await websocket.send("sup")
    res = await websocket.recv()
    res: dict = json.loads(res)
    return res
  
  
if __name__ == '__main__':
    asyncio.run(get_from_websockets)
