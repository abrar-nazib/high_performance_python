import asyncio
import multiprocessing
import os
import time

# Async function to simulate a task
async def handle_messages(queue, worker_id):
    print(f"[Worker {worker_id}] PID {os.getpid()} started.")
    while True:
        if not queue.empty():
            msg = queue.get()
            if msg == "STOP":
                print(f"[Worker {worker_id}] Stopping...")
                break
            print(f"[Worker {worker_id}] Got message: {msg}")
        await asyncio.sleep(0.5)  # let other tasks run

# Process target
def process_target(queue, worker_id):
    asyncio.run(handle_messages(queue, worker_id))

if __name__ == "__main__":
    # Create a multiprocessing.Queue (safe for sharing between processes)
    msg_queue = multiprocessing.Queue()

    # Spawn two processes
    processes = []
    for i in range(2):
        p = multiprocessing.Process(target=process_target, args=(msg_queue, i))
        p.start()
        processes.append(p)

    # Send messages from main process
    for i in range(5):
        msg_queue.put(f"Hello {i} from main")
        time.sleep(1)

    # Tell workers to stop
    msg_queue.put("STOP")
    msg_queue.put("STOP")

    # Wait for processes to exit
    for p in processes:
        p.join()

    print("Main process done.")
