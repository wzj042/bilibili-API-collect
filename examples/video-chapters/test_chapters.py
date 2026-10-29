import json
from pathlib import Path
import unittest
from unittest.mock import patch
import chapters


class ChaptersTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(Path(__file__).with_name('BV1vL411G7N7.json').read_text(encoding='utf-8'))

    def test_captured_replays_match(self):
        expected = self.fixture['capture']['data']['view_points']
        self.assertEqual(len(expected), 6)
        for replay in self.fixture['replays'][1:]:
            self.assertEqual(replay['code'], 0)
            self.assertEqual(replay['data']['view_points'], expected)
        chapters.validate_points(expected, 670)

    def test_empty_is_valid_but_missing_is_error(self):
        self.assertEqual(chapters.validate_points([], 670), [])
        for invalid in [None, {}, '']:
            with self.assertRaises(chapters.ChapterError):
                chapters.validate_points(invalid, 670)

    def test_invalid_times(self):
        for start, end in [(-1, 1), (10, 2), (0, 671), (True, 10), (0, float('nan'))]:
            with self.assertRaises(chapters.ChapterError):
                chapters.validate_points([{'content': 'test', 'from': start, 'to': end}], 670)

    def test_selects_requested_page_and_rejects_wrong_identity(self):
        args = chapters.argparse.Namespace(bvid='BV1vL411G7N7', page=2,
                                          transport='http', credentials='omit')
        video = {'bvid': args.bvid, 'aid': 463665680,
                 'pages': [{'page': 1, 'cid': 10, 'duration': 20},
                           {'page': 2, 'cid': 11, 'duration': 30}]}
        player = {'bvid': args.bvid, 'aid': 463665680, 'cid': 11, 'view_points': []}
        with patch.object(chapters, 'api', side_effect=[video, player]) as api:
            self.assertEqual(chapters.run(args)['cid'], 11)
            self.assertEqual(api.call_args.args[2]['cid'], 11)
        with patch.object(chapters, 'api', side_effect=[video, {**player, 'cid': 10}]):
            with self.assertRaises(chapters.ChapterError):
                chapters.run(args)


if __name__ == '__main__':
    unittest.main()
