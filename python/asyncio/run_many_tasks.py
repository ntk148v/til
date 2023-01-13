import asyncio


async def task_coroutine(index):
    print(f'task {index} is running')
    await asyncio.sleep(2)


async def main():
    print('main coroutine started')
    # start many tasks
    started_tasks = [asyncio.create_task(task_coroutine(i)) for i in range(10)]
    # allow some of the tasks time to start
    await asyncio.sleep(1)
    # get all tasks
    tasks = asyncio.all_tasks()

    for task in tasks:
        print(f'> {task.get_name()}, {task.get_coro()}')

    for task in started_tasks:
        await task

asyncio.run(main())

# main coroutine started
# task 0 is running
# task 1 is running
# task 2 is running
# task 3 is running
# task 4 is running
# task 5 is running
# task 6 is running
# task 7 is running
# task 8 is running
# task 9 is running
# > Task-3, <coroutine object task_coroutine at 0x7fbab1016e30>
# > Task-6, <coroutine object task_coroutine at 0x7fbab0ea4c10>
# > Task-11, <coroutine object task_coroutine at 0x7fbab0ea4e40>
# > Task-2, <coroutine object task_coroutine at 0x7fbab1016ce0>
# > Task-9, <coroutine object task_coroutine at 0x7fbab0ea4d60>
# > Task-4, <coroutine object task_coroutine at 0x7fbab10175a0>
# > Task-7, <coroutine object task_coroutine at 0x7fbab0ea4c80>
# > Task-5, <coroutine object task_coroutine at 0x7fbab0ea49e0>
# > Task-10, <coroutine object task_coroutine at 0x7fbab0ea4dd0>
# > Task-8, <coroutine object task_coroutine at 0x7fbab0ea4cf0>
# > Task-1, <coroutine object main at 0x7fbab1016650>
