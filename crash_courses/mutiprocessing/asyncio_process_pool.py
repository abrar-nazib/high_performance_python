import asyncio
import multiprocessing as mp
import logging
import time
from concurrent.futures import ProcessPoolExecutor
from queue import Empty
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(processName)s %(message)s"
)
logger = logging.getLogger(__name__)


def video_process(queue: mp.Queue, shutdown_event: mp.Event) -> str:
    """Simulate CPU-intensive video processing."""
    process_name = mp.current_process().name
    for i in range(4):
        if shutdown_event.is_set():
            logger.info("Shutdown signal received, exiting")
            break
        time.sleep(1)
        frame = {"frame_id": i, "data": f"Video frame {i}"}
        logger.info(f"Sending: {frame}")
        queue.put(frame)
    return f"{process_name} completed"


def audio_process(queue: mp.Queue, shutdown_event: mp.Event) -> str:
    """Simulate CPU-intensive audio processing."""
    process_name = mp.current_process().name
    for i in range(4):
        if shutdown_event.is_set():
            logger.info("Shutdown signal received, exiting")
            break
        time.sleep(1.5)
        chunk = {"chunk_id": i, "data": f"Audio chunk {i}"}
        logger.info(f"Sending: {chunk}")
        queue.put(chunk)
    return f"{process_name} completed"


async def process_queue(queue: mp.Queue, shutdown_event: mp.Event):
    """Read messages from the queue."""
    while not shutdown_event.is_set():
        try:
            message = queue.get_nowait()
            logger.info(f"Main: Received {message}")
        except Empty:
            await asyncio.sleep(0.1)
        except Exception as e:
            logger.error(f"Error reading queue: {e}")
            break


async def main():
    """Main async function to coordinate tasks."""
    mp.set_start_method("spawn", force=True)

    # Use Manager for safe queue and event sharing
    manager = mp.Manager()
    queue = manager.Queue()
    shutdown_event = manager.Event()

    # Create process pool
    executor = ProcessPoolExecutor(max_workers=2)

    try:
        # Submit tasks
        loop = asyncio.get_event_loop()
        video_future = loop.run_in_executor(
            executor, video_process, queue, shutdown_event
        )
        audio_future = loop.run_in_executor(
            executor, audio_process, queue, shutdown_event
        )
        queue_task = asyncio.create_task(process_queue(queue, shutdown_event))

        # Wait for tasks
        try:
            results = await asyncio.wait_for(
                asyncio.gather(video_future, audio_future, return_exceptions=True),
                timeout=10.0,
            )
            for result in results:
                logger.info(f"Task result: {result}")
        except asyncio.TimeoutError:
            logger.warning("Tasks timed out, signaling shutdown")
            shutdown_event.set()

        # Cancel queue reader
        queue_task.cancel()
        try:
            await queue_task
        except asyncio.CancelledError:
            logger.info("Queue reader cancelled")

    finally:
        # Clean up
        executor.shutdown(wait=True)
        manager.shutdown()  # Clean up Manager resources
        logger.info("Main: Cleanup complete")


if __name__ == "__main__":
    asyncio.run(main())
