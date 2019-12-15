#! python3

from aiohttp import web
import asyncio
import socketio
import time


sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

async def index(request):
    with open('static/test.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

async def credentials(request):
    with open('static/credentials.json') as f:
        return web.Response(text=f.read(), content_type='application/json')

@sio.on("connect")
async def connect(sid, environ):
    print("connect ", sid)
    await sio.emit('validated', room=sid)

@sio.on("listen")
async def listen(sid, key):
    print("VALIDATION ", key)
    while True:
    	await asyncio.sleep(5)
    	await sio.emit('message', {"message": "TEST"}, room=sid)

@sio.on("disconnect")
def disconnect(sid):
    print('disconnect ', sid)

app.router.add_static('/static', 'static')
app.router.add_get('/', index)
app.router.add_post('/credentials.json', credentials)

if __name__ == '__main__':
    web.run_app(app)

