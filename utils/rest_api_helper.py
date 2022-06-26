import requests

class RestApiHTTPError(Exception):
    def __init__(self, status_code, *args: object) -> None:
        super().__init__(*args)
        self.status_code = status_code


def fetch_json(path):
    response = requests.get(path)
    if response.status_code != 200:
        raise RestApiHTTPError(response.status_code)
    return response.json()
    
def fetch(path):
    return requests.get(path)
