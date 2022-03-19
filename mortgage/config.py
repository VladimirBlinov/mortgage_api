import os


def get_api_url():
    host = os.getenv("API")
    port = 5005 if host == "localhost" else 80
    return f"http://{host}:{port}"
