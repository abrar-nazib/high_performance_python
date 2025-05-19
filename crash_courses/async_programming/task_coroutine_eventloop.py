import asyncio


async def make_coffee():
    print("Grinding beans...")
    await asyncio.sleep(2)
    print("Coffee is ready!")


async def set_table():
    print("Setting the table...")
    await asyncio.sleep(1)
    print("Table is set!")


async def main():
    coffee_task = asyncio.create_task(make_coffee())
    table_task = asyncio.create_task(set_table())
    print("Doing other chores")
    await coffee_task # Whenever the coffee task gets to sleep, the next task spins up!
    await table_task



asyncio.run(main())
