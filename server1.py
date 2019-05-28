from aiohttp import web
import socketio
import json

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

async def index(request):
    with open('dashboard.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

@sio.on('channel_b')
async def passData(sid, message):
    # When we receive a new event of type
    # 'message' through a socket.io connection
    # we print the socket ID and the message
    # print("Socket ID: " , sid)
    # print(message)
    await sio.emit('channel_b', message)
    
@sio.on('channel_c')
async def passData(sid, message):
    await sio.emit('channel_c', message)

@sio.on('channel_d')
async def passData(sid, message):
    await sio.emit('channel_d', message)

# We bind our aiohttp endpoint to our app
# router
app.router.add_get('/', index)
app.router.add_static('/static/', path='static', name='static')

# We kick off our server
if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=9999)