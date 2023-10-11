import asyncio
import aiohttp
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskManager:
    def __init__(self, db):
        self.all_tasks = {}
        self.stop_event = asyncio.Event()
        self.db = db

    def add_worker(self, w_ip):
        full_ip = f"http://{w_ip}"
        # TODO regex ip validation
        if full_ip not in self.worker_queue._queue:
            self.worker_queue.put_nowait(full_ip)
            logger.info(f"Added worker: {full_ip}")
        return True

    def run_task(self, id, **kwargs):
        self.all_tasks[id] = {'status': 'pending', **kwargs}
        self.tasks_queue.put_nowait(id)

    def complete_task(self,id,status,results):
        if id in self.all_tasks:
            print("status: ",status)
            self.all_tasks[id]['status'] =status
            self.all_tasks[id]['results'] =results
            if status != "success":
                self.tasks.put_nowait(id)
            return {"status":"success"}
        return {"status":"failed"}

    async def main_process_tasks(self):
        logger.info('Consumer: Running')
        async with aiohttp.ClientSession() as session:
            while not self.stop_event.is_set():
                logger.info('Consumer looking for tasks')
                task_id = await self.tasks_queue.get()
                print(f"Task getted: {task_id}")
                task = self.all_tasks[task_id]
                logger.info(f'Consumer: processing task {task["parameters"]}')
                logger.info('Consumer looking for workers')
                w_ip = await self.worker_queue.get()
                logger.info(f'Consumer: Assigned to {w_ip}')
                params = {"id": task_id, "name": task["name"]}
                self.all_tasks[params["id"]]["status"] = "assigned"
                self.all_tasks[params["id"]]["worker"] = w_ip

                try:
                    async with session.post(w_ip, params=params, json=task["parameters"]) as response:
                        if response.status != 200:
                            self.tasks_queue.put_nowait(params["id"])
                        else:
                            logger.info(f"Consumer: {params['id']} = {await response.json()}")
                except Exception as e:
                    logger.error(f"Consumer: An error occurred for task {params['id']}: {e}")
        logger.info('Consumer: Done')

    async def health_checker(self):
        logger.info('Health Checker: Running')
        async with aiohttp.ClientSession() as session:
            while not self.stop_event.is_set():
                logger.info('Health Checker: Checking...')
                pending_task_ids = [task_id for task_id, task in self.all_tasks.items() if task['status'] == 'assigned']
                for task_id in pending_task_ids:
                    task = self.all_tasks[task_id]
                    worker_ip = task['worker']
                    worker_health_path = os.path.join(worker_ip, "health_check").replace("\\", "/")
                    try:
                        async with session.get(worker_health_path, params={"task_id": task_id}) as response:
                            alive = (await response.json())["alive"]
                            print("alive")
                            if not alive:
                                logger.warning(f'Health Checker: Found failed worker with task {task_id}')
                                task['status'] = "pending"
                                self.tasks_queue.put_nowait(task_id)
                    except Exception as e:
                        logger.error(f"Health Checker: An error occurred for task {task_id}: {e}")

                await asyncio.sleep(5)
        logger.info('Health Checker: Done')

    def run_asyncio_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.run_loop())

    async def run_loop(self):
        self.tasks_queue = asyncio.Queue()
        self.worker_queue = asyncio.Queue()
        await asyncio.gather(self.health_checker(), self.main_process_tasks())


#def stop_server():
    # Wait for asyncio loop thread to finish
    # task_manager.stop_event.set()
    # #thread.join()
    # logger.info("Main process done")