from fastapi import FastAPI
app = FastAPI()
q = []

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print(f"Access to server through: {s.getsockname()[0].strip()}:8000")
s.close()

@app.post("/subscribe/")
async def subscribe(ip:str):
    if ip not in q:
        q.append(ip)

        return {"status": "success"}
    return {"status": "failed"}
@app.get("/get_workers/")
async def get_workers():
    return q