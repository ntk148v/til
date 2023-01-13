import asyncio


async def custom_coro():
    return 2+2


async def main():
    # await for custom coroutine
    result = await custom_coro()
    print(result)

# start the coroutine program
asyncio.run(main())

# 4
