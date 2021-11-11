import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# IP = str(os.getenv("IP"))
# PORT = int(os.getenv("PORT"))
# SERVER_ADDRESS = (IP, PORT)
# print(type(IP))
# print(type(PORT))

IP = "23.111.121.114"
PORT = 12345
# IP = "127.0.0.1"
# PORT = 2222
SERVER_ADDRESS = (IP, PORT)
