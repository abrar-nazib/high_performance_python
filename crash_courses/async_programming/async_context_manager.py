import asyncio


class AsyncConnection:
    async def __aenter__(self):
        print("Opening connection..")
        await asyncio.sleep(0.5)
        print("Connection Open.")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Closing connection...")
        await asyncio.sleep(0.5)
        print("Connection closed")
        # Return false to propagate exception if any
        return False

    async def do_work1(self):
        print("Working... 1")
        for i in range(10):
            await asyncio.sleep(1)
            print(f"Work 1 {i}")
        print("Work done! 1")

    async def do_work2(self):
        print("Working.. 2")
        for i in range(10):
            await asyncio.sleep(1)
            print(f"Work 2 {i}")
        print("Work done! 2")


async def main():
    async with AsyncConnection() as conn:
        # Schedule both tasks
        print("Scheduling tasks..")
        task1 = asyncio.create_task(conn.do_work1())
        task2 = asyncio.create_task(conn.do_work2())

        print("Waiting for tasks to finish")
        await task1
        await task2


asyncio.run(main())
