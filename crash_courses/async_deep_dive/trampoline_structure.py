import asyncio
import datetime

loop = asyncio.get_event_loop()
# loop.set_debug(True)


def print_now():
    print(datetime.datetime.now())


def trampoline(name: str = "") -> None:
    print(name, end=" ")
    print_now()
    loop.call_later(0.5, trampoline, name)


def hog():
    sum = 0
    for i in range(10_000):
        for j in range(10_000):
            sum += j

    return sum


loop.call_soon(trampoline, "First")
loop.call_soon(trampoline, "Second")
loop.call_soon(trampoline, "Third")
loop.call_later(5, hog)
loop.call_later(10, hog)
loop.call_later(15, hog)
loop.call_later(20, loop.stop)


loop.run_forever()
