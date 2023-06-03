import sys

import settings

if __name__ == "__main__":
    # print(sys.argv)
    server_ip= sys.argv[1]

    # subscribe_to_server(server_ip)

    import uvicorn
    uvicorn.run("api:app", host=settings.HOST, port=settings.PORT, reload=True)