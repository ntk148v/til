import asyncio


async def task_coroutine(index):
    print(f'> task {index} executing')
    await asyncio.sleep(2)


async def main():
    print('main coroutine started')
    group_coros = [task_coroutine(i) for i in range(10)]
    await asyncio.gather(*group_coros)
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
# main done
