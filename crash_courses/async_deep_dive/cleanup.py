import asyncio
import signal
import sys
import os


async def my_long_running_app_task():
    """A placeholder for main application logic"""
    try:
        print("Application task started. Press Ctrl+C to initiate shutdown")
        while True:
            await asyncio.sleep(1)  # Simulate ongoing work
            print("Application runnin...")
    except asyncio.CancelledError:
        print("Application task cancelled. Performing Cleanup...")
        # Perfor task-specific cleanup operation
        await asyncio.sleep(0.5)
        print("Application task cleanup complete.")
    except Exception as e:
        print(f"Application task encountered an error {e}")


async def graceful_shutdown(loop:asyncio.EventLoop, signum=None):
    """Handles graceful shutdown of the event loop"""
    if signum:
        print(f"\nReceived signal {signum}. Initiating graceful shutdown...")
    else:
        print("\nInitiating graceful shutdown...")

    # Loop.stop() # If loop.run_forever() was used

    # Cancel all pending tasks
    tasks = [
        t
        for t in asyncio.all_tasks(loop=loop)
        if t is not asyncio.current_task(loop=loop)
    ]

    if tasks:
        print(f"Cancelling {len(tasks)} pending tasks...")

    for task in tasks:
        task.cancel()
    await asyncio.gather(
        *tasks, return_exceptions=True
    )  # Wait for the tasks to finish cancelling
    print("All pending tasks cancelled.")
    
    # Shut down asynchronous generators
    print("Shutting down asynchronous generators...")
    await loop.shutdown_asyncgens()
    print("Asynchronous generators shut down")
    
    # Shut down the default eecutor
    print("Shutting down the default executor (waiting for the blocking tasks)...")
    await loop.shutdown_default_executor(timeout=5)
    print("Default executor shut down")
    
    # Close the event loop
    print("Closing the event loop...")
    loop.close()
    print("Event loop closed")
    
async def main():
    loop = asyncio.get_event_loop()
    
    # Set up signal handlers for graceful shutdown
