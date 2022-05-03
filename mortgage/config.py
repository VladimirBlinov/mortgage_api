import os
from dotenv import load_dotenv

load_dotenv()

ROUND = 0


def get_api_url():
    host = os.getenv("API")
    port = 5005
    return f"http://{host}:{port}"
