import logging;logging.basicConfig(level=logging.INFO)
import asyncio
from aiohttp import web

#主界面
async def index(request):
    return web.Response(text='hello world')

#初始化web
async def init(loop):
    app=web.Application(loop=loop)
    app.router.add_get('/',index)
    host='0.0.0.0'
    port='80'
    await loop.create_server(app.make_handler(),host,port)
    logging.info('server started at http://%s:%s...' % (host,port))

#获取线程池
loop=asyncio.get_event_loop()
asyncio.ensure_future(init(loop))
loop.run_forever()
    
