import asyncio
import aiohttp
import os
import logging
from threading import Thread
from time import sleep

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

workers = asyncio.Queue()
tasks = asyncio.Queue()
all_tasks = {}
stop_event = asyncio.Event()

def add_worker(w_ip):
    full_ip = f"http://{w_ip}"
    # TODO regex ip validation
    if full_ip not in workers._queue:
        workers.put_nowait(full_ip)
        logger.info(f"Added worker: {full_ip}")
    return True


def run_task(id, **kwargs):
    all_tasks[id] = {'status': 'pending', **kwargs}
    tasks.put_nowait(id)


def complete_task(id, status, results):
    if id in all_tasks:
        logger.info(f"Task {id} completed with status: {status}")
        all_tasks[id]['status'] = status
        all_tasks[id]['results'] = results
        if status != "success":
            tasks.put_nowait(id)
        return {"status": "success"}
    return {"status": "failed"}


async def main_process_tasks():
    logger.info('Consumer: Running')
    async with aiohttp.ClientSession() as session:
        while not stop_event.is_set():
            print("a ver")
            task_id = await tasks.get()
            task = all_tasks[task_id]
            logger.info(f'Consumer: processing task {task["parameters"]}')

            w_ip = await workers.get()
            logger.info(f'Consumer: Assigned to {w_ip}')

            params = {"id": task_id, "name": task["name"]}
            all_tasks[params["id"]]["status"] = "assigned"
            all_tasks[params["id"]]["worker"] = w_ip

            try:
                async with session.post(w_ip, params=params, json=task["parameters"]) as response:
                    if response.status != 200:
                        tasks.put_nowait(params["id"])
                    else:
                        logger.info(f"Consumer: {params['id']} = {await response.json()}")
            except Exception as e:
                logger.error(f"Consumer: An error occurred for task {params['id']}: {e}")
    logger.info('Consumer: Done')


async def health_checker():
    logger.info('Health Checker: Running')
    async with aiohttp.ClientSession() as session:
        while not stop_event.is_set():
            logger.info('Health Checker: Checking...')

            pending_task_ids = [task_id for task_id, task in all_tasks.items() if task['status'] == 'assigned']
            for task_id in pending_task_ids:
                task = all_tasks[task_id]
                worker_ip = task['worker']
                worker_health_path = os.path.join(worker_ip, "health_check")

                try:
                    async with session.get(worker_health_path, params={"task_id": task_id}) as response:
                        alive = (await response.json())["alive"]
                        if not alive:
                            logger.warning(f'Health Checker: Found failed worker with task {task_id}')
                            task['status'] = "pending"
                            tasks.put_nowait(task_id)
                except Exception as e:
                    logger.error(f"Health Checker: An error occurred for task {task_id}: {e}")

            await asyncio.sleep(5)
    logger.info('Health Checker: Done')

def run_asyncio_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(asyncio.gather(main_process_tasks(), health_checker()))


logger.info("Starting new thread with asyncio loop")
loop = asyncio.new_event_loop()
thread = Thread(target=run_asyncio_loop, args=(loop,))
thread.start()
logger.info("Asyncio loop thread started")

#def main():
# logger.info("Starting new thread with health checker")
# health_thread = Thread(target=asyncio.run, args=(health_checker(),))
# health_thread.start()
# logger.info("Health checker thread started")

# logger.info("Starting new thread with consumer")
# consumer_thread = Thread(target=asyncio.run, args=(main_process_tasks(),))
# consumer_thread.start()
# logger.info("Consumer thread started")



    # Wait for user input to exit the program
    #input("Press Enter to stop the program...")

def stop_threads():
    # Set the stop event to signal threads to stop
    stop_event.set()
    # Wait for asyncio loop thread to finish
    thread.join()
    
    # Wait for threads to finish
    # consumer_thread.join()
    # health_thread.join()

    logger.info("Main process done")



# if __name__ == "worker2":
#     main()
