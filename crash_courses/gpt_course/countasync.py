import asyncio


async def count(name):
    print(f"{name}: One")
    await asyncio.sleep(0.01)
    print(f"{name}: Two")


async def main():
    await asyncio.gather(count("A"), count("B"), count("C"))


if __name__ == "__main__":
    import time

    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"elapsed {elapsed:0.2f} seconds")
