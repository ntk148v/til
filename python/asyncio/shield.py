import asyncio


async def task_coroutine(index):
    print(f'> task {index} executing')
    value = 2
    await asyncio.sleep(value)
    print(f'> task {index} done after sleep {value} seconds')

# cancel the given task after a moment


async def cancel_task(task):
    # block for a moment
    await asyncio.sleep(1)
    # cancel the task
    cancelled = task.cancel()
    print(f'cancelled: {cancelled}')


async def main():
    print('main coroutine started')
    # create a task
    coro = task_coroutine(1)
    task = asyncio.create_task(coro)
    shielded = asyncio.shield(task)
    #  create a task to cancel the first task
    asyncio.create_task(cancel_task(shielded))

    try:
        result = await shielded
        print(f'> got: {result}')
    except asyncio.cancelledError:
        print('shield was cancelled')

    await asyncio.sleep(0.5)
    print(f'shielded: {shielded}')
    print(f'task: {task}')
    print('main done')

asyncio.run(main())

# main coroutine started
# > task 1 executing
# cancelled: True
# shield was cancelled
# shielded: <Future cancelled>
# task: <Task pending name='Task-2' coro=<task_coroutine() running at .../shield.py:7> wait_for=<Future pending cb=[Task.task_wakeup()]>>
# main done
