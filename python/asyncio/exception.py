import asyncio


async def task_coroutine():
    print('> executing the task')
    await asyncio.sleep(1)
    raise Exception('Something went wrong')


async def main():
    print('main coroutine started')
    task = asyncio.create_task(task_coroutine())
    await asyncio.sleep(2)
    ex = task.exception()
    print(f'got exception: {ex}')
    print('main coroutine done')

asyncio.run(main())


# main coroutine started
# > executing the task
# got exception: Something went wrong
# main coroutine done

# # Without exception() call
# main coroutine started
# > executing the task
# main coroutine done
# Task exception was never retrieved
# future: <Task finished name='Task-2' coro=<task_coroutine() done, defined at ...exception.py:4> exception=Exception('Something went wrong')>
# Traceback (most recent call last):
#   File "...exception.py", line 7, in task_coroutine
#     raise Exception('Something went wrong')
# Exception: Something went wrong
