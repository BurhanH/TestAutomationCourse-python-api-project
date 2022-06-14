import requests

class RestApiHelper:
    def __init__(self, base_url):
        self.base_url = base_url

    def fetch_json(self, path):
        response = requests.get(self.base_url + path)
        if response.status_code != 200:
            raise RuntimeError(f"Invalid result: {response.status_code}")
        return response.json()
    
    def fetch(self, path):
        return requests.get(self.base_url + path)
