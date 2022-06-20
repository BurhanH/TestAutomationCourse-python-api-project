import unittest
from faker import Faker
from random import randint
import requests
import json


def generate_payload():
    fake = Faker()
    for _ in range(10):
        my_dict = {'userName': randint(0, 10000), 'password': '&0rW27EL5I*q'}
        return my_dict


TARGET_API = "https://demoqa.com"
ACCOUNT = '/Account/v1/'
BOOKSTORE = '/BookStore/v1/'
PAYLOAD_EXISTING_USER = json.dumps({'userName': '9kovlev', 'password': '&0rW27EL5I*q'})
PAYLOAD_RANDOM_USER = json.dumps(generate_payload())
HEADERS = {'Content-Type': 'application/json'}
USER_NAME = (json.loads(PAYLOAD_EXISTING_USER))["userName"]

HTTP_OK = 200
HTTP_CREATED = 201
HTTP_NO_CONTENT = 204
HTTP_UNAUTHORIZED = 401
HTTP_NOT_AVAILABLE = 404
HTTP_NOT_ACCEPTABLE = 406

TOKEN = None
USER_ID = None


class TestAccountOptions(unittest.TestCase):

    def test_1_create_new_user(self):
        global USER_ID
        response = requests.post(f'{TARGET_API}{ACCOUNT}User', headers=HEADERS, data=PAYLOAD_EXISTING_USER)
        body = response.json()
        USER_ID = body["userID"]
        self.assertEqual(HTTP_CREATED, response.status_code, 'User not created')

    def test_2_get_token(self):
        global TOKEN
        response = requests.post(f'{TARGET_API}{ACCOUNT}GenerateToken', headers=HEADERS, data=PAYLOAD_EXISTING_USER)
        body = response.json()
        TOKEN = body["token"]
        expected_status = 'Success'
        actual_status = body["status"]
        self.assertEqual(actual_status, expected_status, 'The user is not authorized.')

    def test_3_login_existing_user(self):
        response = requests.post(f'{TARGET_API}{ACCOUNT}Authorized', headers=HEADERS, data=PAYLOAD_EXISTING_USER)
        self.assertEqual(response.status_code, HTTP_OK, 'User can not login')

    def test_4_account_authorized(self):
        response = requests.post(f'{TARGET_API}{ACCOUNT}Authorized', headers=HEADERS, data=PAYLOAD_EXISTING_USER)
        body = response.json()

        self.assertEqual(HTTP_OK, response.status_code)
        self.assertTrue(body)

    def test_5_delete_user(self):
        headers_auth = {'Content-Type': 'application/json',
                        'Authorization': f'Bearer {TOKEN}'}
        response = requests.delete(f'{TARGET_API}{ACCOUNT}User/{USER_ID}', headers=headers_auth)
        actual_status_code = response.status_code
        self.assertEqual(HTTP_NO_CONTENT, actual_status_code, 'The user not deleted.')


if __name__ == '__main__':
    unittest.main()
