import requests
import queue
from threading import Thread
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
    all_tasks[id] = {'params':kwargs,'status':'pending'}
    tasks.put_nowait({"id":id,**kwargs})
def complete_task(id,results):
    if id in all_tasks:
        all_tasks[id]['status'] ="completed"
        all_tasks[id]['results'] =results
        return {"status":"success"}
    return {"status":"failed"}

def main_process_tasks():
    print('Consumer: Running')
    # consume work
    while True:
        # get a unit of work
        parameters = tasks.get()
        print(f'Consumer: processing task {parameters}')

        # check for stop
        if parameters is None:
            break
        w_ip = workers.get()
        print(f'Consumer: Assigned to {w_ip}')
        params  = {"id":parameters.pop("id"),"name":parameters.pop("name")}
        all_tasks[params["id"]]["status"]= "assigned"
        all_tasks[params["id"]]["worker"]= w_ip
        response = requests.post(w_ip,params=params, json=parameters)
        if response.status_code != 200:
            tasks.put_nowait(parameters)
            continue
        # report
        print(f"Consumer: {params['id']} = {response.json()}")
    # all done
    print('Consumer: Done')
print("starting new thread with consumer")
consumer = Thread(target=main_process_tasks)
consumer.start()
print("consumer started")

# consumer.join()
