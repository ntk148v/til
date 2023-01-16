import asyncio
import time


def blocking_task():
    print('> task starting')
    time.sleep(2)
    print('> task done')


async def main():
    print('main running the blocking task')
    loop = asyncio.get_running_loop()
    # execute a function in a separate thread
    await loop.run_in_executor(None, blocking_task)
    print('main doing other things')
    await asyncio.sleep(10)

# run the asyncio
asyncio.run(main())

# main running the blocking task
# > task starting
# > task done
# main doing other things
