import requests
import queue
from threading import Thread
import sys

workers = queue.Queue()
tasks = queue.Queue()
all_tasks =  {}
def add_worker(w_ip):
    full_ip = f"http://{w_ip}"
    # TODO regex ip validation
    if full_ip not in workers.queue:
        workers.put_nowait(full_ip)
        print("after")
    return True
def run_task(id,**kwargs):
    all_tasks[id] = {'status':'pending',**kwargs}
    tasks.put_nowait(id)
def complete_task(id,status,results):
    if id in all_tasks:
        print("status: ",status)
        all_tasks[id]['status'] =status
        all_tasks[id]['results'] =results
        if status != "success":
            tasks.put_nowait(id)
        return {"status":"success"}
    return {"status":"failed"}


def main_process_tasks():
    print('Consumer: Running')
    # consume work
    while True:
        # get a unit of work
        task_id = tasks.get()
        name = all_tasks[task_id]['name']
        parameters = all_tasks[task_id]['parameters']
        print(f'Consumer: processing task {parameters}')

        # check for stop
        if parameters is None:
            break
        w_ip = workers.get()
        print(f'Consumer: Assigned to {w_ip}')
        params  = {"id":task_id,"name":name}
        all_tasks[params["id"]]["status"]= "assigned"
        all_tasks[params["id"]]["worker"]= w_ip
        response = requests.post(w_ip,params=params, json=parameters)
        # TODO try except add task to queue
        if response.status_code != 200:
            tasks.put_nowait(parameters)
            continue
        # report
        print(f"Consumer: {params['id']} = {response.json()}")
    # all done
    print('Consumer: Done')
import os
from time import sleep
def health_checker():
    print('Health Checker: Running')
    # consume work
    while True:
        print('Health Checker: Checking...')

        pending_task = ((task_id,task) for task_id,task in all_tasks.items() if task['status'] == 'assigned')
        for task_id,task in pending_task:
            worker_ip  = task['worker']
            worker_health_path  = os.path.join(worker_ip,"health_check")
            
            response = requests.get(worker_health_path,params={"task_id":task_id})
            alive = response.json()["alive"] 
            print(response.json())
            print(alive)
            if  not alive:
                print('Health Checker: Found failed worker with task ',task_id)

                task['status']  = "pending"
                tasks.put_nowait(task_id)
        sleep(10)

print("starting new thread with consumer")
consumer = Thread(target=main_process_tasks)
consumer.start()
print("consumer started")

print("starting new thread with health checker")
health = Thread(target=health_checker)
health.start()
print("health checker started")



# consumer.join()
