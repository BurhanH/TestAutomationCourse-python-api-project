import unittest
import requests
import pytest
from random import randint
from faker import Faker as Fake
from utils_.colored_messages import yellow_on_red_back as bug_report
from utils_.extract_from_json import json_extractor as json_ex

'''Global variables'''
BASE_URL = 'https://reqres.in/api/'
ALL_USERS = 'users'
REQUEST_PAGE = '?page='
REQUEST_DELAYED = '?delay='
RESOURCES = 'unknown'
REGISTRATION = 'register'
LOGIN = 'login'

HTTP_STATUS_OK = 200
HTTP_STATUS_CREATE = 201
HTTP_STATUS_DELETE = 204
HTTP_STATUS_UNSUCCESSFUL = 400
HTTP_STATUS_NOT_FOUND = 404

TEST_DATA = {
    'name': Fake().name(),
    'job':  Fake().job(),
    "email": "eve.holt@reqres.in",
    "password": Fake().password()
}

TEST_DATA_UPD = {
    'name': Fake().name(),
    'job': Fake().job()
}

ERR_MESSAGE = {
    "error": "Missing password"
}


class TestReqresAPI(unittest.TestCase):

    @pytest.mark.reqres
    def test_1_check_list_users_pages(self):
        """Getting the default list of users. Determining the number of pages and users."""
        response = requests.get(f'{BASE_URL}{ALL_USERS}')
        self.assertEqual(response.status_code, HTTP_STATUS_OK, bug_report('Bad request total user page.'))
        total_user_pages = (response.json())['total_pages']
        self.assertGreater(total_user_pages, 0, bug_report('The user database is not filled.'))
        total_users = (response.json())['total']
        self.assertGreater(total_users, 0, bug_report('No one user has been created.'))

        """Getting a complete list of users in a global variable."""
        all_users_data = []
        for page_num in range(1, total_user_pages + 1):
            response_users = requests.get(f'{BASE_URL}{ALL_USERS}{REQUEST_PAGE}{page_num}')
            self.assertEqual(response_users.status_code,
                             HTTP_STATUS_OK,
                             bug_report(f'Bad request user page #{page_num}'))
            all_users_data.extend(response_users.json()['data'])

        """Checking invalid page call values"""
        invalid_user_pages = [randint(-100, -2), -1, 0, total_user_pages + 1, total_user_pages + randint(2, 100)]
        for num in invalid_user_pages:
            check_page = requests.get(f'{BASE_URL}{ALL_USERS}{REQUEST_PAGE}{num}')
            self.assertEqual(check_page.status_code, HTTP_STATUS_OK, bug_report(f'Bad request user page #{num}.'))
            if check_page.json()['data']:
                print(bug_report(f'BUG!!! In user\'s list page {num} are not empty.'))
            else:
                self.assertFalse(check_page.json()['data'], bug_report(f'In user\'s list page {num} are not empty.'))

        """Valid random user info"""
        test_user = randint(1, total_users)
        response_user = requests.get(f'{BASE_URL}{ALL_USERS}/{test_user}')
        self.assertEqual(response_user.status_code, HTTP_STATUS_OK, bug_report(f'Bad request user {test_user}'))
        self.assertIn(response_user.json()['data'], all_users_data, f'User #{test_user} data is missing.')

        """Check non existent user request"""
        non_existent_user = [randint(-100, -2), -1, 0, total_users + 1, total_users + randint(2, 100)]
        for i in non_existent_user:
            check_user = requests.get(f'{BASE_URL}{ALL_USERS}/{i}')
            self.assertEqual(check_user.status_code, HTTP_STATUS_NOT_FOUND, bug_report(f'User #{i} already exists.'))
            self.assertFalse(check_user.json(), bug_report(f'Non existent user #{i} already exists.'))

    @pytest.mark.reqres
    def test_2_check_list_resource_pages(self):
        """Getting the default list of resources. Determining the number of ID resources."""
        response = requests.get(f'{BASE_URL}{RESOURCES}')
        self.assertEqual(response.status_code, HTTP_STATUS_OK, bug_report('Bad request total resources page.'))
        total_res = (response.json())['total']
        self.assertGreater(total_res, 0, bug_report('No one resource has been created.'))

        """Valid random resource info"""
        res_id = randint(1, total_res)
        response_res = requests.get(f'{BASE_URL}{RESOURCES}/{res_id}')
        self.assertEqual(response_res.status_code, HTTP_STATUS_OK, bug_report(f'Bad request user {res_id}'))
        self.assertIsNotNone(response_res.json()['data'], bug_report(f'Data of resource #{res_id} is None.'))

        """Check non existent resource request"""
        non_existent_res = [randint(-100, -2), -1, 0, total_res + 1, total_res + randint(2, 100)]
        for res_id in non_existent_res:
            check_res = requests.get(f'{BASE_URL}{RESOURCES}/{res_id}')
            self.assertEqual(check_res.status_code, HTTP_STATUS_NOT_FOUND, bug_report(f'Res.#{res_id} already exists.'))
            self.assertFalse(check_res.json(), bug_report(f'Res. #{res_id} already exists.'))

    @pytest.mark.reqres
    def test_3_CrUD_user(self):
        """Creating a user"""
        response_create = requests.post(f'{BASE_URL}{ALL_USERS}', json=json_ex(TEST_DATA, 'name', 'job'))
        self.assertEqual(response_create.status_code, HTTP_STATUS_CREATE, bug_report('Bad request to create user.'))
        self.assertIsNotNone(response_create.json()['createdAt'], bug_report(f'Test user not created.'))
        self.assertIsNotNone(response_create.json()['id'])
        test_user_id = response_create.json()['id']

        """Updating the user by the PUT method"""
        response_put = requests.put(f'{BASE_URL}{ALL_USERS}/{test_user_id}', json=json_ex(TEST_DATA_UPD, 'name'))
        self.assertEqual(response_put.status_code, HTTP_STATUS_OK, bug_report('Bad request to update user by the PUT.'))
        self.assertIsNotNone(response_put.json()['updatedAt'], bug_report('Test user name not updated by the PUT.'))

        """Updating the user by the PATCH method"""
        response_patch = requests.patch(f'{BASE_URL}{ALL_USERS}/{test_user_id}', json=json_ex(TEST_DATA_UPD, 'job'))
        self.assertEqual(response_patch.status_code,
                         HTTP_STATUS_OK,
                         bug_report('Bad request to update user by the PATCH.'))
        self.assertIsNotNone(response_patch.json()['updatedAt'],
                             bug_report('Test user job not updated by the PATCH method.'))

        """Deleting a user"""
        response_delete = requests.delete(f'{BASE_URL}{ALL_USERS}/{test_user_id}')
        self.assertEqual(response_delete.status_code, HTTP_STATUS_DELETE, bug_report('Bad request to delete user.'))
        check_delete = requests.get(f'{BASE_URL}{ALL_USERS}/{test_user_id}')
        self.assertEqual(check_delete.status_code,
                         HTTP_STATUS_NOT_FOUND,
                         bug_report(f'User #{test_user_id} has not be deleted.'))

    @pytest.mark.reqres
    def test_4_registration(self):
        """Registration successful"""
        response_reg = requests.post(f'{BASE_URL}{REGISTRATION}', json=json_ex(TEST_DATA, 'email', 'password'))
        self.assertEqual(response_reg.status_code, HTTP_STATUS_OK, bug_report('Bad request to register user.'))
        self.assertTrue(response_reg.json()['token'], bug_report('Token is not exists.'))

        """Registration unsuccessful"""
        response_bad = requests.post(f'{BASE_URL}{REGISTRATION}', json=json_ex(TEST_DATA, 'email'))
        self.assertEqual(response_bad.status_code,
                         HTTP_STATUS_UNSUCCESSFUL,
                         bug_report('User registered without a PWD.'))
        self.assertTrue(response_bad.json()['error'], bug_report('There is no error message.'))
        self.assertEqual(response_bad.json(), ERR_MESSAGE, bug_report('The error message is wrong.'))

    @pytest.mark.reqres
    def test_5_login(self):
        """Registration successful"""
        response_login = requests.post(f'{BASE_URL}{LOGIN}', json=json_ex(TEST_DATA, 'email', 'password'))
        self.assertEqual(response_login.status_code, HTTP_STATUS_OK, bug_report('Bad request to login user.'))
        self.assertTrue(response_login.json()['token'], bug_report('Token is not exists.'))

        """Registration unsuccessful"""
        response_bad = requests.post(f'{BASE_URL}{REGISTRATION}', json=json_ex(TEST_DATA, 'email'))
        self.assertEqual(response_bad.status_code, HTTP_STATUS_UNSUCCESSFUL, bug_report('User logged without a PWD.'))
        self.assertTrue(response_bad.json()['error'], bug_report('There is no error message.'))
        self.assertEqual(response_bad.json(), ERR_MESSAGE, bug_report('The error message is wrong.'))

    @pytest.mark.reqres
    def test_6_check_delayed_response(self):
        """Checking delayed page calls"""
        check_delay = requests.get(f'{BASE_URL}{ALL_USERS}{REQUEST_DELAYED}3')
        self.assertEqual(check_delay.status_code, HTTP_STATUS_OK, bug_report(f'Bad delayed request.'))
