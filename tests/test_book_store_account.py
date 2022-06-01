import unittest

import requests
import json

TARGET_API = "https://demoqa.com"
ACCOUNT = '/Account/v1/'
BOOKSTORE = '/BookStore/v1/'
PAYLOAD = json.dumps({"userName": "test7", "password": "Te$t$tudent13"})
HEADERS = {'Content-Type': 'application/json'}
USER_NAME = (json.loads(PAYLOAD))["userName"]

HTTP_OK = 200
HTTP_CREATED = 201
HTTP_NO_CONTENT = 204
HTTP_UNAUTHORIZED = 401
HTTP_NOT_AVAILABLE = 404
HTTP_NOT_ACCEPTABLE = 406

TOKEN = None
USER_ID = None


class TestBookStore(unittest.TestCase):
    @staticmethod
    def check_ability_gen_token():
        """check is is possible to generate token.
        If user not exists then
        status = failed
        result = User authorization failed.
        """
        response = requests.post(f'{TARGET_API}{ACCOUNT}GenerateToken', headers=HEADERS, data=PAYLOAD)
        body = response.json()
        return True if body["status"] == "Success" else False

    def test_1_user_create(self):
        """create new user"""
        global USER_ID
        response = requests.post(f'{TARGET_API}{ACCOUNT}User', headers=HEADERS, data=PAYLOAD)
        body = response.json()
        actual_user_name = body["username"]

        if response.status_code == HTTP_CREATED:
            USER_ID = body["userID"]
            self.assertEqual(HTTP_CREATED, response.status_code)
            self.assertEqual(USER_NAME, actual_user_name,
                             f"Desired user name '{USER_NAME}' is not equals to just created '{actual_user_name}'")
        else:
            self.assertTrue(response.status_code in [HTTP_NOT_AVAILABLE, HTTP_NOT_ACCEPTABLE],
                            f"unexpected response code {response.status_code}!")
            self.assertEqual("User exists!", body["message"],
                             f'User already created before, this operation failed but error message '
                             f'"{body["message"]}" not equal to "User exists!"')

    def test_2_generate_token(self):
        """Generate token"""
        global TOKEN
        response = requests.post(f'{TARGET_API}{ACCOUNT}GenerateToken', headers=HEADERS, data=PAYLOAD)
        body = response.json()
        TOKEN = body["token"]

        self.assertEqual(response.status_code, HTTP_OK)
        self.assertEqual(body["status"], "Success")
        self.assertEqual(body["result"], "User authorized successfully.")

    def test_3_login(self):
        """user login"""
        global TOKEN

        response = requests.post(f'{TARGET_API}{ACCOUNT}Login', headers=HEADERS, data=PAYLOAD)
        body = response.json()
        TOKEN = body["token"]

        self.assertEqual(USER_NAME, body["username"])

    def test_4_account_authorized(self):
        """checking user logged in or not"""
        response = requests.post(f'{TARGET_API}{ACCOUNT}Authorized', headers=HEADERS, data=PAYLOAD)
        body = response.json()

        self.assertEqual(HTTP_OK, response.status_code)
        self.assertTrue(body)

    def test_5_user_delete(self):
        """delete user"""
        headers_auth = {'Content-Type': 'application/json',
                        'Authorization': f'Bearer {TOKEN}'}

        response = requests.delete(f'{TARGET_API}{ACCOUNT}User/{USER_ID}', headers=headers_auth)
        status_code = response.status_code

        if status_code == HTTP_NO_CONTENT:
            self.assertFalse(self.check_ability_gen_token())
        elif status_code == HTTP_OK:
            self.assertTrue(self.check_ability_gen_token(),
                            f'Account not deleted! Status code{status_code}, but operation could not complete!')
        else:
            self.assertTrue(self.check_ability_gen_token(),
                            f'Unexpected Error on user deletion, status code: "{status_code}"!')


if __name__ == '__main__':
    unittest.main()
