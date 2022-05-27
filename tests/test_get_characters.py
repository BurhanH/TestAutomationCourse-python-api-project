import unittest
import requests
BASE_URL = "https://www.breakingbadapi.com/api/"


class TestCharacters(unittest.TestCase):

    def test_all_characters(self):
        response = requests.get(BASE_URL + "characters")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(len(body) > 0)
        for character in body:
            self._check_character(character)

    def test_single_character(self):
        response = requests.get(BASE_URL + "characters/1")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(len(body), 1)
        self.assertEqual(body[0]["char_id"], 1)
        self._check_character(body[0])

    def test_single_character_invalid_id(self):
        response = requests.get(BASE_URL + "characters/invalid_id")
        self.assertNotEqual(response.status_code, 200)

    def test_single_character_not_existing(self):
        response = requests.get(BASE_URL + "characters")
        body = response.json()
        num = max([i["char_id"] for i in body])
        response = requests.get(BASE_URL + "characters/" + str(num + 1))
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(len(body), 0)

    def test_character_by_category(self):
        response = requests.get(BASE_URL + "characters/?category=Better+Call+Saul")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(len(body) > 0)
        for character in body:
            self._check_character(character)
            self.assertTrue("Better Call Saul" in character["category"])
    
    def test_character_by_category_limit(self):
        response = requests.get(BASE_URL + "characters/?category=Better+Call+Saul&limit=2")
        self.assertEqual(response.status_code, 200)
        body1 = response.json()
        self.assertTrue(len(body1) <= 2)
        response = requests.get(BASE_URL + "characters/?category=Better+Call+Saul&limit=2&offset=2")
        self.assertEqual(response.status_code, 200)
        body2 = response.json()
        self.assertNotEqual(body1, body2)

    #cheking character attributes
    def _check_character(self, character):
        self.assertTrue("char_id" in character)
        self.assertTrue("name" in character)
        self.assertTrue("birthday" in character)
        self.assertTrue("occupation" in character)
        self.assertTrue("img" in character)
        self.assertTrue("status" in character)
        self.assertTrue("appearance" in character)
        self.assertTrue("nickname" in character)
        self.assertTrue("portrayed" in character)


if __name__ == '__main__':
    unittest.main()
