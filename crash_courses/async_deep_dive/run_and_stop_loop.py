import asyncio


async def greet(name):
    await asyncio.sleep(1)  # Simulate I/O work
    print(f"Hello, {name}!")
    return f"Greeting for {name} complete."


def run_until_complete_synchronous_example():
    # This function demonstrates loop.run_until_complete() from a synchronous context.
    # It is crucial NOT to wrap this call with asyncio.run() directly,
    # as asyncio.run() itself manages an event loop.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)  # Set this loop as the current one for the context

    try:
        print("Starting loop with run_until_complete from synchronous context...")
        # Schedule the coroutine and run the loop until it finishes
        # No 'await' here because loop.run_until_complete is a synchronous call
        # when called directly on the loop object from a non-async function.
        result = loop.run_until_complete(greet("Alice"))
        print(f"Task finished: {result}")
    finally:
        # It is crucial to close the loop when done to release resources.
        loop.close()
        print("Loop closed.")


# To run this example, execute:
run_until_complete_synchronous_example()

# Note: For most applications, asyncio.run() is the preferred high-level entry point.
# If you are already inside an async function managed by asyncio.run(),
# you would simply await your coroutine directly:
#
# async def main_high_level_example():
#     print("Starting high-level example...")
#     result = await greet("Bob") # No need for loop.run_until_complete() here
#     print(f"Task finished: {result}")
#
# # To run this high-level example:
# # asyncio.run(main_high_level_example())
