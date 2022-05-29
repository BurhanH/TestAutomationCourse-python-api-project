import unittest
import requests
URL = "https://www.breakingbadapi.com/api/"


class TestGetQuotes(unittest.TestCase):

    def test_get_all_quotes(self):
        response = requests.get(f'{URL}quotes')
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(len(body), 70, 'The length of body is not equal 70')

    def test_get_quote_by_id(self):
        response = requests.get(f'{URL}quotes/1')
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body[0]['quote_id'], 1, 'Wrong quote id')
        for quote in body:
            self._check_quote_attr(quote)

    def test_get_quotes_by_series(self):
        response = requests.get(f'{URL}quote?series=Better+Call+Saul')
        self.assertEqual(response.status_code, 200)
        body = response.json()
        print(body)

    def test_get_random_quote(self):
        response1 = requests.get(f'{URL}quote/random')
        self.assertEqual(response1.status_code, 200)
        body1 = response1.json()
        self.assertEqual(len(body1), 1, 'The length of body is not equal to expected value')
        response2 = requests.get(f'{URL}quote/random')
        body2 = response2.json()
        self.assertNotEqual(body1, body2, "It's not a random quote")

    def test_get_all_quotes_by_author(self):
        response = requests.get(f'{URL}quote?author=Jesse+Pinkman')
        self.assertEqual(response.status_code, 200)
        body = response.json()
        count = 0
        for i in range(len(body)):
            self.assertEqual(body[i]['author'],  'Jesse Pinkman')

    def test_get_random_quote_from_author(self):
        response = requests.get(f'{URL}quote/random?author=Skyler+White')
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(len(body), 1)
        self.assertEqual(body[0]['author'], 'Skyler White')

    def _check_quote_attr(self, quote):
        self.assertTrue('quote_id' in quote)
        self.assertTrue('quote' in quote)
        self.assertTrue('author' in quote)
        self.assertTrue('series' in quote)

    def tearDown(self) -> None:
        pass

if __name__ == '__main__':
    unittest.main
