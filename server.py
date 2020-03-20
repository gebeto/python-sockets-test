#! python3

from aiohttp import web
import asyncio
import socketio
import json


app = web.Application()
print(dir(app))

exit(0)

sio = socketio.AsyncServer()
sio.attach(app)

data_users = {}

async def users(request):
    data = json.dumps(data_users)
    return web.Response(text=data, content_type='application/json')

async def notify(request):
    sid = request.query.get("si/d", None)
    data = await request.read()

    if sid and message:
        asyncio.ensure_future(
            sio.emit('message', {"message": message}, room=sid)
        )

    return web.Response(text='', content_type='application/json')


@sio.on("connect")
async def connect(sid, environ):
    print("CONNECT ", sid)
    data_users[sid] = {}

# @sio.on("listen")
# async def listen(sid, key):
#     print("VALIDATION ", sid, key)
#     while True:
#     	await asyncio.sleep(5)
#     	await sio.emit('message', {"message": "TEST"}, room=sid)

@sio.on("disconnect")
def disconnect(sid):
    del data_users[sid]
    print('DISCONNECT ', sid)

app.router.add_get('/', users)
app.router.add_post('/notify', notify)

if __name__ == '__main__':
    web.run_app(app, port=5000)

