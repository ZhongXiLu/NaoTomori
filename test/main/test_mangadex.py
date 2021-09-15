import unittest
from dataclasses import dataclass
from unittest.mock import patch

from requests import Session

from naotomori.cogs.source.manga.mangadex import MangaDex


@dataclass
class Response:
    """
    Source: dataclass to store information for an anime/manga.
    """

    status_code: int
    text: str


class TestMangaDex(unittest.TestCase):
    """Tests for the MangaDex"""

    def setUp(self):
        self.mangadex = MangaDex()

    def mock_response(self, url):
        if url.startswith("https://api.mangadex.org/chapter"):
            with open('test/main/test_data/mangadex_chapter.json') as file:
                return Response(200, file.read())
        elif url.startswith("https://api.mangadex.org/manga"):
            with open('test/main/test_data/mangadex_manga.json') as file:
                return Response(200, file.read())
        else:
            return Response(400, "{}")

    @patch.object(Session, 'get', mock_response)
    def test_getRecentManga(self):
        """Test getting the most recent manga from the MangaDex homepage"""

        recentManga = self.mangadex.getRecent()
        self.assertEqual(len(recentManga), 16)
        self.assertEqual([anime.title for anime in recentManga], [
            'CHR-47',
            'CHR-47',
            'CHR-47',
            'Affairs of the Enchanting Doctor',
            'Affairs of the Enchanting Doctor',
            'Affairs of the Enchanting Doctor',
            'The Disappearing Classroom',
            'The Disappearing Classroom',
            'The Disappearing Classroom',
            'Marriage in a Heartbeat',
            'Marriage in a Heartbeat',
            'Marriage in a Heartbeat',
            'Don’t Get Me Wrong, I’m The Real Victim!',
            'Don’t Get Me Wrong, I’m The Real Victim!',
            'Don’t Get Me Wrong, I’m The Real Victim!',
            'This Contract Romance Must Not Turn Real!'
        ])
        self.assertEqual([anime.progress for anime in recentManga[:10]], [
            'Chapter 7',
            'Chapter 8',
            'Chapter 9',
            'Chapter 23',
            'Chapter 24',
            'Chapter 25',
            'Chapter 23.1',
            'Chapter 24.2',
            'Chapter 24.1',
            'Chapter 30.1'
        ])
        self.assertEqual([anime.link for anime in recentManga[:10]], [
            'https://mangadex.org/chapter/18ed7d22-d189-4f54-8344-d3891acd54ce',
            'https://mangadex.org/chapter/c04cb411-df37-4f60-817d-606556b91077',
            'https://mangadex.org/chapter/003701a4-5462-4f6f-a811-e2924cd9d31c',
            'https://mangadex.org/chapter/63b19198-a3b9-4f99-b03b-358347b1ef53',
            'https://mangadex.org/chapter/200a6fc5-a734-4f56-b779-c202acaf5cc2',
            'https://mangadex.org/chapter/c2c487a6-b5c9-4f4a-9edc-a2b03a3959ff',
            'https://mangadex.org/chapter/9f10a60b-5099-4fef-ae6d-c32991810db9',
            'https://mangadex.org/chapter/6c903e07-651d-4f3f-8a93-4685eb030818',
            'https://mangadex.org/chapter/1a95ef04-253e-4f17-9018-45fada6005eb',
            'https://mangadex.org/chapter/b43bc657-d23f-4f98-9c4a-16ef742f4d6c'
        ])
