import coroweb

@coroweb.web_func(path='/',method='GET')
async def index(*args,**kw):
    return 'hello world!'

index_handler=coroweb.RequestHandler(index)

