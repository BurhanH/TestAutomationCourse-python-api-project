import unittest
import requests
BASE_URL = "https://www.breakingbadapi.com/api/"

class RestApiTestCaseBase(unittest.TestCase):
    def fetch_json(self, path):
        response = requests.get(BASE_URL + path)
        self.assertEqual(response.status_code, 200)
        return response.json()
    
    def fetch(self, path):
        return requests.get(BASE_URL + path)
