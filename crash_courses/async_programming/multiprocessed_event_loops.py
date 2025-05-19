import asyncio
import multiprocessing
import os


async def worker_task(worker_id):
    print(f"[Worker {worker_id}] PID {os.getpid()}: Starting task")
    for i in range(5):
        await asyncio.sleep(1)
        print(f"[Worker {worker_id}] Tick {i}")
    print(f"[Worker {worker_id}] Done")


def run_event_loop(worker_id):
    # Each process runs its own asyncio event loop
    asyncio.run(worker_task(worker_id))


if __name__ == "__main__":
    num_processes = 4
    processes = []

    for i in range(num_processes):
        p = multiprocessing.Process(target=run_event_loop, args=(i,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
