import asyncio
import orm
from models import User,Blog,Comment

async def save(loop):
    await orm.create_pool(loop,password='testTest_2',db='awesome',user='test')
    u=User(name='test',email='test@example',passwd='123456',image='about:blank',loop=loop)
    await u.save()
    await orm.destroy_pool()

loop=asyncio.get_event_loop()
loop.run_until_complete(save(loop))
loop.close()


