import unittest
import requests


BASE_URL = 'https://www.breakingbadapi.com/api/'
HTTP_OK = 200
TOTTAL_EPISODES = 102

class TestEpisodes(unittest.TestCase):

    def _check_episodes_attr(self, episode):
        self.assertTrue("episode_id" in episode)
        self.assertTrue("title" in episode)
        self.assertTrue("season" in episode)
        self.assertTrue("episode" in episode)
        self.assertTrue("air_date" in episode)
        self.assertTrue("characters" in episode)
        self.assertTrue("series" in episode)


    def test_get_all_episodes(self):
        response = requests.get(f'{BASE_URL}episodes')
        self.assertEqual(response.status_code, HTTP_OK)
        self.assertEqual(
            len(response.json()),
            TOTTAL_EPISODES,
            f'expected fetch data about {TOTTAL_EPISODES} episodes'
        )
        body = response.json()
        for episode in body:
            self._check_episodes_attr(episode)

    def test_get_episode_by_id(self):
        response = requests.get(f'{BASE_URL}episodes/3')
        self.assertEqual(response.status_code, HTTP_OK)
        body = response.json()
        self.assertEqual(len(body), 1)
        self.assertEqual(body[0]["episode_id"], 3, 'Wrong episode id')
        self.assertEqual(body[0]["title"], "...And the Bag's in the River", 'Wrong title value')
        self.assertEqual(body[0]["air_date"], "02-10-2008", 'Wrong air_date value')

    def test_get_episode_by_series(self):
        series = "Better Call Saul"
        response = requests.get(f'{BASE_URL}episodes?series=Better+Call+Saul')
        self.assertEqual(response.status_code, HTTP_OK)
        body = response.json()
        self.assertTrue(len(body) > 0)
        for episode in body:
            self._check_episodes_attr(episode)
            self.assertTrue(series == episode["series"], f'{series} series is not found')
        self.assertEqual(body[0]["characters"], ["Jimmy McGill", "Mike Erhmantraut",
                                                 "Kim Wexler", "Howard Hamlin", "Chuck McGill", "Nacho Varga"])

    def test_episodes_by_part_name_of_series(self):
        series = "Breaking"
        response = requests.get(f'{BASE_URL}episodes?series=Breaking+Bad')
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(len(body) > 0)
        for episode in body:
            self._check_episodes_attr(episode)
            self.assertTrue(series in episode["series"], f'{series} is not found in series')

    def test_episode_title_in_data(self):
        episodeTitle = "Ozymandias"
        response = requests.get(f'{BASE_URL}episodes')
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(len(body) > 0)
        titleInBody = None
        for episode in body:
            if episodeTitle == episode["title"]:
                titleInBody = True
                break
        self.assertTrue(titleInBody, f'{episodeTitle} is not found')


if __name__ == '__main__':
    unittest.main()
