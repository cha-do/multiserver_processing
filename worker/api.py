from fastapi import FastAPI
import sys
from network import network
import logic
import settings
from threading import Thread

# subscribe_to_server,send_results
app = FastAPI()

@app.get("/")
async def get_workers():
    return {'hi':'worker running'}

@app.post("/")
async def run_task(id:str,name:str,parameters:dict):
    resolver_class = getattr(logic, settings.DEFAULT_RESOLVER)
    resolver_obj = resolver_class()
    passtask = False
    for task in settings.tasks:
        if task.task_id == id:
            task = resolver_obj
            passtask = True
            break
    if not passtask:
        settings.tasks.append(resolver_obj)

    t = Thread(target=resolver_obj.run,args=(id,name,parameters))
    t.start()
    return {'status':'assigned'}

@app.get("/validate_task")
async def validate_task(id:str):
    for task in settings.tasks:
        if task.task_id == id:
            return task.status
    return {"status": "failed","message":"task not found"}

@app.get("/all_tasks")
async def all_task():
    return settings.tasks


@app.get("/health_check")
async def health_check(task_id:str):
    alive = False
    for task in settings.tasks:
        if task.task_id == task_id:
            print(f"task {task_id} status: {task.status}")
            alive = task.status != "failed"
            break
    print("check alive: ",alive)
    return {"alive":alive}

network.subscribe_to_server(sys.argv[1])

def run():
    return 1#/0


