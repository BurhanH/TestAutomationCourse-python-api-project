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

    def test_character_by_random(self):
        response = requests.get(BASE_URL + "character/random")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(len(body) == 1)

    def test_character_limit_offset(self):
        offset = 0
        step = 50
        count = 10
        while count > 0:
            response = requests.get(BASE_URL + f"characters?limit={step}&offset={offset}")
            self.assertEqual(response.status_code, 200)
            body = response.json()
            offset += step
            count = len(body)
            self.assertTrue(len(body) <= step)

    def test_character_invalid_limit(self):
        step = -10
        response = requests.get(BASE_URL + f"characters?limit={step}")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(len(body) == 0)

    def test_character_by_name(self):
        response = requests.get(BASE_URL + "characters/?name=Walter+White")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(len(body) == 1)
        self._check_character(body[0])
        self.assertEqual(body[0]["name"], "Walter White")

    def test_character_by_invalid_name(self):
        name = "unknown"
        response = requests.get(BASE_URL + f"characters/?name={name}")
        print(response.json())
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(len(body) == 0)

    def test_character_by_part_name(self):
        response = requests.get(BASE_URL + "characters/?name=Walter")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(len(body) > 0)
        for character in body:
            self._check_character(character)
            self.assertTrue("Walter" in character["name"])

    #checking character attributes
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
