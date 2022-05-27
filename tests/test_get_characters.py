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
        print (body)
        self.assertEqual(len(body), 1)
        self.assertEqual(body[0]["char_id"], 1)
        self._check_character(body[0])

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
