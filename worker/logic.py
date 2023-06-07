

import time
from network import network 
import sys

class TaskResolver:
    def __init__(self) -> None:
        self.task_id = None
        self.status = None
    def run(self,id,name,parameters):
        try:
            self.task_id = id
            self.status = "running"
            results = self._run(name,parameters)
            self.status = results.pop("status")
            print("status: ",self.status)
            network.send_results(self.task_id, results=results,status=self.status)
                

        except Exception as e:
            print(e)
            self.status = "failed"
            network.send_results(self.task_id,results=e.args[0],status="failed")

        network.subscribe_to_server(sys.argv[1])
        
class CalculatorTaskResolver(TaskResolver):
    def __init__(self) -> None:
        self.functions = {
            'sum': lambda parameters:sum(parameters["numbers"]),
            'divide': lambda parameters:parameters["a"]/parameters["parameters"]["b"],
            'multiply': lambda parameters:parameters["a"]*parameters["parameters"]["b"],
            'subtract': lambda parameters: parameters["a"]-parameters["parameters"]["b"]
        }
    def _run(self,name,parameters):
        print(f"hi we are running the next task {self.task_id} {name}, with parameters {parameters}")
        time.sleep(20)
        if name in self.functions:
            print(parameters)
            result = self.functions[name](parameters)
            print(result)
            return {'status':'success','result':result}
        return {'status':'failed','message':"unrecognized function"}
        
class MetaauristicasTaskResolver(TaskResolver):
    
    def __run(self,id,name,parameters):
        pass

