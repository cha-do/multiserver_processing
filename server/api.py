from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import worker2 as workers

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print(f"Access to server through: {s.getsockname()[0].strip()}:8000")
s.close()
app = FastAPI()





@app.post("/subscribe/")
async def subscribe(ip:str):
    
        if workers.add_worker(ip):

        # response = requests.get(ip)
        # if response.status_code == 200:
        # else:
        #     raise HTTPException(status_code=403)
            return {"status": "success"}
        return {"status": "failed"}

@app.get("/get_workers/")
async def get_workers():
    return workers.workers.queue

@app.get("/get_tasks/")
async def get_tasks():
    return workers.all_tasks

@app.post("/complete_task/")
async def complete_task(id:str,status:str,results:dict):
    return workers.complete_task(id,status,results)





@app.post("/runtask/")
async def runtask(id:str,name:str,parameters:dict):
    print(f"running task {id} {name} with params {parameters}")
    response = workers.run_task(id=id,name=name,parameters=parameters)

    return response

input("PRESS ENTER TO STOP THE PROGRAM.\n")
workers.stop_threads()
