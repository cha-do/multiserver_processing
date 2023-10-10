from dotenv import load_dotenv
import os
import sys

load_dotenv()

# print(os.environ)
HOST =os.environ["HOST"]
if len(sys.argv) >= 3:
    PORT = int(sys.argv[2])
else:
    PORT = os.environ["PORT"]

if len(sys.argv) >= 4:
    DEFAULT_RESOLVER = sys.argv[3]
else:
    DEFAULT_RESOLVER = os.environ["DEFAULT_RESOLVER"]
tasks = []