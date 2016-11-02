#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

__author__='huobao'

import functools

#get,post装饰函数
def web_func(path='/',method='GET'):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args,**kw):
            return func(*args,**kw)
        wrapper.__path__=path
        wrapper.__method__=method
        return wrapper
    return decorator

#解析参数
async def parse_param(request):
    params={}
    #解析路径参数
    path_request=request.match_info
    for k, v in path_request.items():
        params[k]=v
    
    ##解析请求参数
    if request.method == 'POST':
        post_params=await request.post()
        for k,v in post_params.items():
            params[k]=v
    elif request.method=='GET':
        query_str=request.query_string
        if query_str:
            query_tube=query_str.split('&')
            for query in query_tube:
                query_tube_each=query.split('=')
                params[query_tube_each[0]]=params[query_tube_each[1]]
    else:
        logging.error('the %s method is unsupported!' % request.method)
        raise Exception()
    return params;


#处理函数
class RequestHandler:
    def __init__(self,func):
        self.func=func
    
    #解析请求参数
    async def __call__(self,request):
        #解析请求参数
        kw=await parse_param(request)
        #调用func
        r=await self.func(kw)
        return r


