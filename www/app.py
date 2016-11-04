#!/usr/bin/env python3.5

# -*- coding: utf-8 -*-

__author__='huobo'

import logging;logging.basicConfig(level=logging.INFO)
import asyncio,json
from aiohttp import web
from coroweb import RequestHandler
import handler
from jinja2 import Environment, FileSystemLoader

#拦截处理方法.请求处理前和处理后进行拦截
async def middleware_factory(app, handler):
    async def middleware_handler(request):
        #处理请求之前
        #处理请求
        r=await handler(request)
        #未完待续
        #构建response
        if isinstance(r,web.Response):
            return r
        elif isinstance(r,web.StreamResponse):
            return r
        elif isinstance(r,str):
            return web.Response(text=r,content_type='text/plain',charset='utf-8')
        elif isinstance(r,bytearray):
            return web.Response(body=bytearray,content_type='application/octet-stream')
        elif isinstance(r,dict):
            template = r.get('__template__')
            if template:
                resp = web.Response(body=app['__templating__'].get_template(template).render(r).encode('utf-8'))
                resp.content_type = 'text/html;charset=utf-8'
                return resp
            else:
                resp = web.Response(body=json.dumps(r, ensure_ascii=False, default=lambda o: o.__dict__).encode('utf-8'))
                resp.content_type = 'application/json;charset=utf-8'
                return resp
        else:
            logging.error('response data type %s is unsupport!' % type(r))
            web.Response(status=415)
    return middleware_handler


#主界面
def add_handler(app,handler):
    if isinstance(handler,RequestHandler):
        method=handler.func.__method__
        path=handler.func.__path__
        if method=='GET':
            app.router.add_route(method,path,handler)
        elif method=='POST':
            app.router.add_route(method,path,handler)
        else:
            logging.error('the %s method of the http is not support!' % method)
    else:
        logging.error('handler is not RequestHandler!')
        raise Exception('handler is not RequestHandler1')


#添加处理函数
def add_router(app,handler_file):
    modules=__import__(handler_file)
    for attr in dir(modules):
        if attr.startswith('__'):
            continue
        fun=getattr(modules,attr)
        method=getattr(fun,'__method__',None)
        path=getattr(fun,'__path__',None)
        if method and path:
            logging.info('add handler %s' % attr)
            add_handler(app,RequestHandler(fun))

#初始化jinja模板
def init_template(app,template_file):
    env = Environment(loader=FileSystemLoader(template_file))
    app['__templating__'] = env


#初始化web
async def init(loop):
    app=web.Application(loop=loop,middlewares=[middleware_factory])
    add_router(app,'handler')
    init_template(app,'../templates')
    host='0.0.0.0'
    port='80'
    await loop.create_server(app.make_handler(),host,port)
    logging.info('server started at http://%s:%s...' % (host,port))

#获取线程池
loop=asyncio.get_event_loop()
asyncio.ensure_future(init(loop))
loop.run_forever()
    
