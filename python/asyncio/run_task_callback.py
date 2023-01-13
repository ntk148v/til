import asyncio


def callback(task):
    print('this is a callback of', task)


async def task_coroutine():
    print('execute the task')
    # wait for a bit
    await asyncio.sleep(2)


async def main():
    print('main coroutine started')
    # create and schedule the task
    task = asyncio.create_task(task_coroutine())
    task.add_done_callback(callback)
    # wait for the task to complete
    await task
    print('main coroutine done')


# start the asyncio program
asyncio.run(main())

# main coroutine started
# execute the task
# this is a callback of <Task finished name='Task-2' coro=<task_coroutine() done, defined at /.../run_task_callback.py:8> result=None>
# main coroutine done
