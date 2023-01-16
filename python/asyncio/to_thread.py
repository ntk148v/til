import asyncio
import time


def blocking_task():
    print('> task starting')
    time.sleep(2)
    print('> task done')


async def main():
    print('main running the blocking task')
    # to_thread creates a ThreadPoolExecutor behind the scenes
    # to execute blocking calls
    coro = asyncio.to_thread(blocking_task)
    task = asyncio.create_task(coro)
    print('main doing other things')
    await asyncio.sleep(1)
    await task

# run the asyncio
asyncio.run(main())

# main running the blocking task
# main doing other things
# > task starting
# > task done
