

import settings
import requests
import os.path
class NetworkManager:
    def __init__(self) -> None:
        
        self.worker_ip  = self.get_lan_ip()
        self.server_ip = None

    def get_lan_ip(self):
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))

        ip =  s.getsockname()[0].strip()
        s.close()
        return ip


    def subscribe_to_server(self,pserver_ip):
        self.server_ip = f"http://{pserver_ip}"
        params = {
            'ip': f"{self.worker_ip}:{settings.PORT}",
        }
        print(f"suscribing to server {self.server_ip} with the params {params}")
        url = os.path.join(self.server_ip,"subscribe").replace("\\", "/")
        response = requests.post(url, params=params)
        if  response.status_code != 200 or response.json()['status'] != 'success':
            raise Exception("We couldn't connect to server")
        print(f"Connected to server on ip {self.server_ip} ")

    def send_results(self,id,results,status="success"):
        print("sending results to server = ",results)
        url_responses = os.path.join(self.server_ip,"complete_task").replace("\\", "/")
        r = requests.post(url_responses,params={"id":id,"status":status},json=results)
        print("server response = ",r.json())

   
network  =NetworkManager()
