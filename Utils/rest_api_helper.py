import requests


def fetch_json(path):
    response = requests.get(path)
    if response.status_code != 200:
        raise RuntimeError(f"Invalid result: {response.status_code}")
    return response.json()


def fetch(path):
    return requests.get(path)
