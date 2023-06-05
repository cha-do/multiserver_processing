from fastapi import FastAPI
import sys
from network import NetworkManager 
network  =NetworkManager()
# subscribe_to_server,send_results
app = FastAPI()




@app.get("/")
async def get_workers():
    return {'hi':'worker running'}

import time
from threading import Thread
import requests
from random import randint
def run_task_logic(id,name,parameters):
    print(f"hi we are running the next task {id} {name}, with parameters {parameters}")
    time.sleep(3)
    print(f"process done.")
    print(parameters)
    network.send_results(id,results={"result":sum(parameters["parameters"]["numbers"])})
    network.subscribe_to_server(sys.argv[1])

@app.post("/")
async def run_task(id:str,name:str,parameters:dict):

    t = Thread(target=run_task_logic,args=(id,name,parameters))
    t.start()
    return {'status':'success'}

network.subscribe_to_server(sys.argv[1])
