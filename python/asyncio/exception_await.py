import asyncio


async def task_coroutine():
    print('> executing the task')
    await asyncio.sleep(1)
    raise Exception('Something went wrong')


async def main():
    print('main coroutine started')
    task = asyncio.create_task(task_coroutine())
    try:
        await task
    except Exception as ex:
        print(f'got exception: {ex}')
    print('main coroutine done')

asyncio.run(main())

# main coroutine started
# > executing the task
# got exception: Something went wrong
# main coroutine done
