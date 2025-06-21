import multiprocessing as mp
import time
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format="%(processName)s: %(message)s")
logger = logging.getLogger(__name__)


def sender_process(queue: mp.Queue, shutdown_event: mp.Event):
    """Process that sends message to the receiver."""
    try:
        for i in range(5):
            if shutdown_event.is_set():
                logger.info("Shutdown signal received, exiting")
                break

            message = {"id": i, "data": f"Message {i} from sender"}
            logger.info(f"Sending: {message}")
            queue.put(message)
            time.sleep(1)
        queue.put({"id": -1, "data": "END"})
    except Exception as e:
        logger.error(f"Error in sender: {e}")


def receiver_process(queue: mp.Queue, shutdown_event: mp.Event):
    try:
        while not shutdown_event.is_set():
            try:
                if not queue.empty():
                    message: Dict[str, Any] = queue.get()
                    logger.info(f"Redceived: {message}")
                    if message["id"] == -1 and message["data"] == "END":
                        logger.info("End message received, exiting")
                        break
                    logger.info(f"Processing message {message['id']}")
            except Exception as e:
                logger.error(f"Error in receiver {e}")
            time.sleep(0.1)
    except Exception as e:
        logger.error(f"Error in receiver {e}")


def main():
    """Main function to set up and run processes."""

    # Create queue for message exchange
    queue = mp.Queue()
    # Create shutdown event to signal process termination
    shutdown_event = mp.Event()

    sender = mp.Process(
        target=sender_process, args=(queue, shutdown_event), name="Sender"
    )

    receiver = mp.Process(
        target=receiver_process, args=(queue, shutdown_event), name="Receiver"
    )

    try:
        sender.start()
        receiver.start()

        time.sleep(6)

        # Signal shutdown
        logger.info("Main: Signaling shutdown")
        shutdown_event.set()
        sender.join(timeout=2)
        receiver.join(timeout=2)

        if sender.is_alive():
            logger.warning("Sender did not terminate, forcing exit")
            sender.terminate()
        if receiver.is_alive():
            logger.warning("Receiver did not terminate, forcing exit")
            receiver.terminate()
    finally:
        queue.close()
        queue.join_thread()
        logger.info("Main: Cleanup complete")


if __name__ == "__main__":
    main()
