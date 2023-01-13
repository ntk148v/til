import asyncio


async def task_coroutine():
    print('execute the task')
    # wait for a bit
    await asyncio.sleep(2)


async def main():
    print('main coroutine started')
    # create and schedule the task
    task = asyncio.create_task(task_coroutine())
    # wait for the task to complete
    await task
    print('main coroutine done')


# start the asyncio program
asyncio.run(main())
