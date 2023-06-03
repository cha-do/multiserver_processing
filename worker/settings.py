from dotenv import load_dotenv

import os
load_dotenv()


# print(os.environ)
HOST =os.environ["HOST"]
PORT = int(os.environ["PORT"])