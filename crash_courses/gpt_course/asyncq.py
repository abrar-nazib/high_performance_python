import asyncio


async def producer(name, queue, wait_time, num_items):
    """Put items in the queue with fixed timing"""
    for i in range(num_items):
        await asyncio.sleep(wait_time)  # Fixed wait time
        item = f"{name}{i}"
        await queue.put(item)
        print(f"[{name}] produced: {item}")


async def consumer(name, queue, process_time):
    """Take items from the queue with fixed timing"""
    while True:
        item = await queue.get()
        print(f"[{name}] consuming: {item}")
        await asyncio.sleep(process_time)  # Fixed processing time
        print(f"[{name}] finished: {item}")
        queue.task_done()


async def main():
    queue = asyncio.Queue()

    # Producer A: produces every 2 seconds, makes 3 items
    # Producer B: produces every 3 seconds, makes 2 items
    producers = [
        asyncio.create_task(producer("A", queue, wait_time=2, num_items=3)),
        asyncio.create_task(producer("B", queue, wait_time=3, num_items=2)),
    ]

    # Consumer X: processes items in 1 second
    # Consumer Y: processes items in 2 seconds
    consumers = [
        asyncio.create_task(consumer("X", queue, process_time=1)),
        asyncio.create_task(consumer("Y", queue, process_time=2)),
    ]

    await asyncio.gather(*producers)
    await queue.join()

    for c in consumers:
        c.cancel()


asyncio.run(main())
