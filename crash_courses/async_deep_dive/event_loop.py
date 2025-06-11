import asyncio


loop = asyncio.get_event_loop()

print(loop)

loop.run_until_complete(asyncio.sleep(5))

import datetime


def print_now():
    print(datetime.datetime.now())


loop.call_soon(print_now)  # Register to the event loop now
loop.call_later(8, print_now)  # Register to the event loop to be run 8 seconds later
# loop.run_until_complete(asyncio.sleep(10))


def trampoline(name: str = "") -> None:
    print(name, end=" ")
    print_now()
    loop.call_later(0.5, trampoline, name)


loop.call_soon(trampoline)

loop.call_later(18, loop.stop)

loop.run_forever()
