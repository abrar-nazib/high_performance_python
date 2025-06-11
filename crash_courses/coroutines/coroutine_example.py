import asyncio
import datetime
import time


def print_now():
    print(datetime.datetime.now())


async def keep_printing(name: str = "") -> None:
    while True:
        print(name, end=" ")
        print_now()
        try:
            await asyncio.sleep(0.50)
        except asyncio.CancelledError:
            print(name, "was cancelled")
            break  # Actually cancel


async def async_main() -> None:
    try:
        await asyncio.wait_for(
            asyncio.gather(
                keep_printing("First"), keep_printing("Second"), keep_printing("Third")
            ),
            5,
        )
    except asyncio.TimeoutError:
        print("Timeout occured")


asyncio.run(async_main())
