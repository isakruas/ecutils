import json
import logging
import uvicorn
from fastapi import (
    FastAPI,
    WebSocket
)


app = FastAPI(title='Elliptic Curve Cryptography')

CHANNELS = dict()


async def notify(channel):
    if CHANNELS[channel]:
        message = json.dumps({'users': len(CHANNELS[channel])})
        [await user.send_text(message) for user in CHANNELS[channel]]


async def register(user, channel):
    if CHANNELS.get(channel, None) is None:
        CHANNELS[channel] = set()
    CHANNELS[channel].add(user)
    await notify(channel)


async def unregister(user, channel: str):
    CHANNELS[channel].remove(user)
    await notify(channel)


@app.websocket("/ecc/{channel}/")
async def server(channel, websocket: WebSocket):
    await websocket.accept()
    await register(websocket, channel)
    while True:
        try:
            data = await websocket.receive_text()
            if CHANNELS[channel]:
                [await user.send_text(data) for user in CHANNELS[channel] if user != websocket]
        except Exception as err:
            logging.info(err)
            await unregister(websocket, channel)
            break


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=1998)
