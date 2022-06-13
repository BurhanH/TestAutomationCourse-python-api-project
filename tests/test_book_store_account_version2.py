import unittest
import time
import requests
import json

TARGET_API = "https://demoqa.com"
ACCOUNT = '/Account/v1/'
BOOKSTORE = '/BookStore/v1/'
PAYLOAD = {
    "login": {"userName": "test77", "password": "Te$t$Tudent13"},
    "create_user": {"userName": "test8", "password": "Te$t$Tudent13"},
    "authorize_user": {"userName": "test9", "password": "Te$t$Tudent13"},
    "get_token": {"userName": "test10", "password": "Te$t$Tudent13"},
    "get_user": {"userName": "test11", "password": "Te$t$Tudent13"},
    "delete": {"userName": "test12", "password": "Te$t$Tudent13"},
}

HEADERS = {'Content-Type': 'application/json'}

HTTP_OK = 200
HTTP_CREATED = 201
HTTP_NO_CONTENT = 204
HTTP_UNAUTHORIZED = 401
HTTP_NOT_AVAILABLE = 404
HTTP_NOT_ACCEPTABLE = 406


class TestBookStore(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        payload = json.dumps(PAYLOAD["login"])
        cls.create_user(payload)

    @classmethod
    def tearDownClass(cls):
        resp = cls.login(cls)
        cls.delete_user(user_id=resp.json()['userId'], token=resp.json()['token'])

    def setUp(self):
        self.login(self)

    @staticmethod
    def login(self):
        response = requests.post(f'{TARGET_API}{ACCOUNT}Login', headers=HEADERS, data=json.dumps(PAYLOAD["login"]))
        return response

    @staticmethod
    def create_user(payload):
        response = requests.post(f'{TARGET_API}{ACCOUNT}User', headers=HEADERS, data=payload)
        return response

    @staticmethod
    def delete_user(user_id, token):
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
        return requests.delete(f'{TARGET_API}{ACCOUNT}User/{user_id}', headers=headers)

    @staticmethod
    def gen_token(payload):
        response = requests.post(f'{TARGET_API}{ACCOUNT}GenerateToken', headers=HEADERS, data=payload)
        return response

    @staticmethod
    def user_get(payload, user_id):
        response = requests.post(f'{TARGET_API}{ACCOUNT}GenerateToken', headers=HEADERS, data=payload)
        body = response.json()
        token = body["token"]
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
        return requests.get(f'{TARGET_API}{ACCOUNT}User/{user_id}', headers=headers)

    def test_z_authorized(self):
        """Authorized user"""
        payload = json.dumps(PAYLOAD["login"])
        response = requests.post(f'{TARGET_API}{ACCOUNT}Authorized', headers=HEADERS, data=payload)
        body = response.json()

        self.assertEqual(HTTP_OK, response.status_code)
        self.assertTrue(body)

    def test_generate_token(self):
        """Generate token"""
        payload = json.dumps(PAYLOAD["login"])
        response = requests.post(f'{TARGET_API}{ACCOUNT}GenerateToken', headers=HEADERS, data=payload)
        body = response.json()

        self.assertEqual(response.status_code, HTTP_OK)
        self.assertEqual(body["status"], "Success")
        self.assertEqual(body["result"], "User authorized successfully.")

    def test_user_create(self):
        """create new user"""
        payload = json.dumps(PAYLOAD["create_user"])
        response = self.create_user(payload)

        body = response.json()
        user_id = body["userID"]

        self.assertEqual(response.status_code, HTTP_CREATED)
        self.assertEqual(PAYLOAD["create_user"]["userName"], body["username"])

        # clean up
        token = self.gen_token(payload).json()['token']
        self.delete_user(user_id, token)

    def test_user_get(self):
        """get new user info"""
        payload = json.dumps(PAYLOAD["get_user"])
        response = self.create_user(payload)
        body = response.json()

        user_id = body["userID"]

        self.assertEqual(response.status_code, HTTP_CREATED)
        self.assertEqual(PAYLOAD["get_user"]["userName"], body["username"])

        token = self.gen_token(payload).json()['token']
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}

        response = requests.get(f'{TARGET_API}{ACCOUNT}User/{user_id}', headers=headers, data=payload)
        body = response.json()

        self.assertEqual(response.status_code, HTTP_OK)
        self.assertEqual(PAYLOAD["get_user"]["userName"], body["username"])

        # clean up
        self.delete_user(user_id, token)

    def test_delete(self):
        """delete new user"""

        payload = json.dumps(PAYLOAD["delete"])
        response = self.create_user(payload)

        body = response.json()
        user_id = body["userID"]

        self.assertEqual(response.status_code, HTTP_CREATED)
        self.assertEqual(PAYLOAD["delete"]["userName"], body["username"])

        token = self.gen_token(payload).json()['token']

        response = self.delete_user(user_id, token)
        self.assertEqual(response.status_code, HTTP_NO_CONTENT)


if __name__ == '__main__':
    unittest.main()
