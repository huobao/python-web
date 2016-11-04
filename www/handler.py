import coroweb

@coroweb.web_func(path='/',method='GET')
async def index(*args,**kw):
    return 'hello world!'

@coroweb.web_func(path='/food',method='GET')
async def template_index(*args,**kw):
    food_dict={}
    food_dict['__template__']='food'
    food_dict['apple']='red'
    food_dict['pear']='yellow'
    return food_dict
