import unittest
import requests
import json

BASE_URL = 'https://restful-booker.herokuapp.com/'
HEADER = {'Content-Type': 'application/json'}
PAYLOAD = json.dumps({'username': 'admin', 'password': 'password123'})
PAYLOAD_CREATE_BOOKING = json.dumps({
    "firstname": "Testbooking",
    "lastname": "Bookingtest",
    "totalprice": 145,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2022-04-25",
        "checkout": "2022-05-01"
    },
    "additionalneeds": "Stake"
})

PAYLOAD_UPDATE_BOOKING = json.dumps({
    "firstname": "Testbooking",
    "lastname": "Bookingtest",
    "totalprice": 145,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2022-05-25",
        "checkout": "2022-06-01"
    },
    "additionalneeds": "Breakfast"
})

PAYLOAD_PARTIAL_UPDATE = json.dumps({"firstname": "Thomas",
    "lastname": "Edison"})

FIRST_NAME = "Testbooking"
LAST_NAME = "Bookingtest"
F_NAME = "Thomas"
L_NAME = "Edison"
TOTAL_PRICE = 145
DEPOSIT = True
ADDITIONAL = "Stake"
HTTP_Success = 200
HTTP_CREATED = 201
TOKEN = None
BOOKINGID = None


class TestRestfulBooker(unittest.TestCase):

    def test_1_create_auth_token(self):
        """Generate token"""
        global TOKEN
        response = requests.post(f'{BASE_URL}auth', headers=HEADER, data=PAYLOAD)
        body = response.json()
        TOKEN = body['token']
        self.assertEqual(response.status_code, HTTP_Success)

    def test_2_get_booking_ids(self):
        """Get all booking ids"""
        response = requests.get(f'{BASE_URL}booking')
        body = response.json()
        body_json = json.dumps(body, indent=2)
        if response.status_code == HTTP_Success:
            self.assertTrue(len(body_json) > 0)

    def test_3_create_booking(self):
        """Create booking"""
        global BOOKINGID
        response = requests.post(f'{BASE_URL}booking', headers=HEADER, data=PAYLOAD_CREATE_BOOKING)
        body = response.json()
        BOOKINGID = body['bookingid']
        self.assertEqual(response.status_code, HTTP_Success)
        self.assertTrue("bookingid" in body)

    def test_4_get_booking_filter_by_id(self):
        """Get booking filter by id"""
        global BOOKINGID
        response = requests.get(f'{BASE_URL}booking/{BOOKINGID}')
        body = response.json()
        self.assertEqual(body['firstname'], FIRST_NAME)
        self.assertEqual(body['lastname'], LAST_NAME)
        self.assertEqual(body['totalprice'], TOTAL_PRICE)
        self.assertEqual(body['depositpaid'], DEPOSIT)
        self.assertEqual(body['additionalneeds'], ADDITIONAL)

    def test_5_update_booking(self):
        global BOOKINGID
        header_auth = {'Content-Type': 'application/json',
                        'Accept': 'application/json',
                        'Cookie': f'token={TOKEN}'}
        response = requests.put(f'{BASE_URL}booking/{BOOKINGID}', headers=header_auth,
                                data=PAYLOAD_UPDATE_BOOKING)
        body = response.json()
        self.assertEqual(body["bookingdates"]["checkin"], "2022-05-25")
        self.assertEqual(body["bookingdates"]["checkout"], "2022-06-01")

    def test_6_partial_update(self):
        global BOOKINGID
        header_auth = {'Content-Type': 'application/json',
                        'Accept': 'application/json',
                        'Cookie': f'token={TOKEN}'}
        response = requests.patch(f'{BASE_URL}booking/{BOOKINGID}', headers=header_auth,
                                  data=PAYLOAD_PARTIAL_UPDATE)
        body = response.json()
        self.assertTrue(response.status_code, HTTP_Success)
        self.assertEqual(body["firstname"], F_NAME)
        self.assertEqual(body["lastname"], L_NAME)

    def test_7_delete_booking(self):
        global BOOKINGID
        header_del_auth = {'Content-Type': 'application/json',
                       'Cookie': f'token={TOKEN}'}
        response = requests.delete(f'{BASE_URL}booking/{BOOKINGID}', headers=header_del_auth)
        self.assertEqual(response.status_code, HTTP_CREATED)


if __name__ == '__main__':
    unittest.main()