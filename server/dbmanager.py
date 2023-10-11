from pydantic import BaseModel

class TaskModel(BaseModel):
    id: str
    name: str
    parameters: dict
    status: str
    worker: str

class WorkerModel(BaseModel):
    id: str
    ip: str
