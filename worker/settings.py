from dotenv import load_dotenv

import os
import sys
load_dotenv()


# print(os.environ)
HOST =os.environ["HOST"]
PORT = int(sys.argv[2])