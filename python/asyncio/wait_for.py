import asyncio


async def task_coroutine(index):
    print(f'> task {index} executing')
    value = 2
    await asyncio.sleep(value)
    print(f'> task {index} done after sleep {value} seconds')


async def main():
    print('main coroutine started')
    # create a task
    coro = task_coroutine(1)

    try:
        # you can change timeout and sleep (in task_coroutine)
        # to play with it
        await asyncio.wait_for(coro, timeout=3)
        print('main done')
    except asyncio.TimeoutError:
        print('main gave up waiting , task cancelled')

asyncio.run(main())

# main coroutine started
# > task 1 executing
# main gave up waiting , task cancelled
