import asyncio
import datetime
import time


def print_now():
    print(datetime.datetime.now())


async def keep_printing(name: str = "") -> None:
    while True:
        print(name, end=" ")
        print_now()
        await asyncio.sleep(0.50)


# async def async_main() -> None:
#     try:
#         await asyncio.wait_for(keep_printing("Hey"), 10)
#     except asyncio.TimeoutError:
#         print("OOps, Time's up")


async def async_main() -> None:
    kp = keep_printing("Hello!") #
    print(kp)
    waiter = asyncio.wait_for(kp, 3)
    print(waiter)
    try:
        await waiter
    except asyncio.TimeoutError:
        print("Time's out!")


asyncio.run(async_main())
