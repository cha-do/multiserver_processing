
tasks = [
    {
        "name":"add",
        "parameters":{
            "numbers":[1,2,3,4]
            }
    },
        {
        "name":"divide",
        "parameters":{
            "a":2,
            "b":4
            }
    }
]
##Task example
# tasks.put_nowait(1)
    # all_tasks[1]={
    #     "name":"sum",
    #     "parameters":{
    #         "numbers":[4,2,3]
    #         },
    #     'status' : "pending"
    # }


# import custom_multiprocessing
import requests
for params in tasks:
    r  =requests.post("http://localhost:8000/runtask",params=params)
    print(f"task {params['name']} = {r.status_code}")
