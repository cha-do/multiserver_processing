from fastapi import FastAPI
import requests
import sys
import settings
app = FastAPI()



def get_lan_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))

    ip =  s.getsockname()[0].strip()
    s.close()
    return ip


def subscribe_to_server(server_ip):
    params = {
        'ip': f"{get_lan_ip()}:{settings.PORT}",
    }
    print(f"suscribing to server {server_ip} with the params {params}")

    url = f'http://{server_ip}/subscribe/'
    response = requests.post(url, params=params)
    if  response.status_code != 200 or response.json()['status'] != 'success':
        raise Exception("Whe couldn't connect to server")
    print(f"Connected to server on ip {server_ip} ")

@app.get("/")
async def get_workers():
    return {'hi':'worker running'}

import time
@app.post("/")
async def run_task(id:str,name:str,parameters:dict):
    print(f"hi we are running the next task {id} {name}, with parameters {parameters}")
    time.sleep(20)
    print(f"process done.")

    return {'status':'success'}

subscribe_to_server(sys.argv[1])
