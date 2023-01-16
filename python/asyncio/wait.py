import asyncio
import random


async def task_coroutine(index):
    value = random.random()
    print(f'> task {index} executing')
    await asyncio.sleep(value)
    print(f'> task {index} done after sleep {value} seconds')


async def main():
    print('main coroutine started')
    tasks = [asyncio.create_task(task_coroutine(i)) for i in range(10)]
    # wait for all tasks to complete
    done, pending = await asyncio.wait(tasks)
    # wait for the first tasks to complete
    # done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    # wait for the first tasks to failed
    # done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)
    # you can play with done and pending
    print('main done')

asyncio.run(main())

# main coroutine started
# > task 0 executing
# > task 1 executing
# > task 2 executing
# > task 3 executing
# > task 4 executing
# > task 5 executing
# > task 6 executing
# > task 7 executing
# > task 8 executing
# > task 9 executing
# > task 4 done after sleep 0.02505134629289052 seconds
# > task 0 done after sleep 0.15302129609152493 seconds
# > task 8 done after sleep 0.1565534467066032 seconds
# > task 5 done after sleep 0.1676313361328544 seconds
# > task 1 done after sleep 0.3886707880704876 seconds
# > task 3 done after sleep 0.45932413337182765 seconds
# > task 6 done after sleep 0.5445482469243019 seconds
# > task 2 done after sleep 0.6234779487073143 seconds
# > task 9 done after sleep 0.7615839933532805 seconds
# > task 7 done after sleep 0.7726912337045355 seconds
# main done
