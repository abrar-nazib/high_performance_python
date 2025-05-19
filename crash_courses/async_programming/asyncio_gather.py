import asyncio


async def task1():
    print(f"Initiating task 1")
    await asyncio.sleep(1)
    print("Task 1 done")


async def task2():
    print("Initiating task 2")
    await asyncio.sleep(2)
    print("Task 2 done")


async def main():
    await asyncio.gather(task1(), task2())


asyncio.run(main())
