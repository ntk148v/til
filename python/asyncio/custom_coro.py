async def custom_coro():
    return 2+2


async def main():
    # await for custom coroutine
    result = await custom_coro()
    print(result)


m = main()
# not executed yet; coro is a coroutine, not 4
print(type(m))

# <class 'coroutine'>
# sys:1: RuntimeWarning: coroutine 'main' was never awaited
