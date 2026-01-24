import unittest
from src.processing.data_cleaner import process_data

class TestPipeline(unittest.TestCase):

    def test_clean_steam_data(self):
        data = [
            {'appid': 1, 'name': 'Game1', 'playtime_forever': 100, 'last_played': None, 'fetched_at': '2023-01-01'}
        ]
        df = process_data('steam', data)
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]['appid'], 1)

    def test_clean_mal_data(self):
        data = [
            {'mal_id': 1, 'title': 'Anime1', 'status': 'completed', 'score': 8, 'fetched_at': '2023-01-01'}
        ]
        df = process_data('mal', data)
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]['mal_id'], 1)

if __name__ == '__main__':
    unittest.main()