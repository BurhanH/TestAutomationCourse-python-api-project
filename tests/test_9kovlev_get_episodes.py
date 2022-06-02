import unittest
import requests

BASE_URL = "https://www.breakingbadapi.com/api/"


class TestCharacters(unittest.TestCase):

    def test_first_episoode(self):
        response = requests.get(BASE_URL + "episodes/1")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(len(body), 1)
        self.assertEqual(body[0]["episode_id"], 1)
        for keys in body:
            self.check_keys(keys)

    def test_test_first_episoode_invalid_id(self):
        response = requests.get(BASE_URL + "episodes/invalid_id")
        self.assertNotEqual(response.status_code, 200)

    def test_first_episoode_by_title(self):
        response = requests.get(BASE_URL + "episodes/1")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(len(body) > 0)
        for keys in body:
            self.check_keys(keys)
            self.assertTrue("Pilot" in keys["title"])

    def test_episoode_by_series(self):
        response = requests.get(BASE_URL + "episodes?series=Better+Call+Saul")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(len(body) == 40)
        self.check_keys(body[0])
        self.assertEqual(body[0]["series"], "Better Call Saul")

    # checking character attributes
    def check_keys(self, keys):
        self.assertTrue("episode_id" in keys)
        self.assertTrue("title" in keys)
        self.assertTrue("season" in keys)
        self.assertTrue("air_date" in keys)
        self.assertTrue("characters" in keys)


if __name__ == '__main__':
    unittest.main()
