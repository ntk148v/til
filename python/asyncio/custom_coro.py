import asyncio


async def custom_coro():
    # await for another coroutine
    await asyncio.sleep(1)

# create the coroutine
coro = custom_coro()
print(type(coro))
