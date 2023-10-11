from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import worker
import socket
import logging
from threading import Thread
from motor.motor_asyncio import AsyncIOMotorClient

#Connect to MongoDB database
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["task_manager"]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_server_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0].strip()
    s.close()
    return ip

app = FastAPI()

@app.post("/subscribe/")
async def subscribe(ip:str):
    
        if task_manager.add_worker(ip):

        # response = requests.get(ip)
        # if response.status_code == 200:
        # else:
        #     raise HTTPException(status_code=403)
            return {"status": "success"}
        return {"status": "failed"}

@app.get("/get_workers/")
async def get_workers():
    return task_manager.worker_queue._queue

@app.get("/get_tasks/")
async def get_tasks():
    return task_manager.all_tasks

@app.post("/complete_task/")
async def complete_task(id:str,status:str,results:dict):
    return task_manager.complete_task(id,status,results)

@app.post("/runtask/")
async def runtask(id:str,name:str,parameters:dict):
    print(f"running task {id} {name} with params {parameters}")
    response = task_manager.run_task(id=id,name=name,parameters=parameters)
    return response

@app.get("/stop_server/")
async def stop_server():
    task_manager.stop_event.set()
    #thread.join()
    logger.info("Main process done")
    return {"respose":"server done"}

#input("PRESS ENTER TO STOP THE PROGRAM.\n")
#workers.stop_threads()
#if __name__ == "__main__":
ip_address = get_server_ip()
logger.info(f"Access the server through: {ip_address}:8000")

# Create an instance of TaskManager
task_manager = worker.TaskManager(db)

# Run the asyncio loop in a separate thread
logger.info("Starting new thread with asyncio loop")
thread = Thread(target=task_manager.run_asyncio_loop)
thread.start()
logger.info("Asyncio loop thread started")
    
