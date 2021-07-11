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
            'Eko Eko Azaraku: Reborn',
            'Rivnes',
            'Young Black Jack',
            'The Princess is Evil',
            'Fate/Grand Order - Daily Chaldea (Doujinshi)',
            'Orenchi ni Kita Onna Kishi to Inakagurashi Surukotoninatta Ken',
            'I Met the Male Lead in Prison',
            'Badass',
            'Hawkwood',
            'Lovetrap Island - Passion in Distant Lands -',

            # Note that there are multiple chapters released at once for the same manga
            'Saki',
            'Saki',
            'Saki',
            'Saki',

            "My Life as Inukai-san's Dog",
            "I'm a former slave, but I tried to buy an oni slave who I later found to "
            'have too much energy so I want to throw him away...'
        ])
        self.assertEqual([anime.progress for anime in recentManga[:10]], [
            'Chapter 13',
            'Chapter 19.5',
            'Chapter 17',
            'Chapter 23',
            'Chapter 804',
            'Chapter 59',
            'Chapter 20',
            'Chapter 7',
            'Chapter 45',
            'Chapter 8'
        ])
        self.assertEqual([anime.link for anime in recentManga[:10]], [
            'https://mangadex.org/chapter/42afb8c9-58bb-4fa3-8459-087a542c9770',
            'https://mangadex.org/chapter/a1165340-ecf0-4f39-96d0-589baa887ee5',
            'https://mangadex.org/chapter/fce3e504-4490-4f56-bfbb-be2ab6f1b16c',
            'https://mangadex.org/chapter/181dd654-e4c9-4f72-a9a6-1df9a37ccd3e',
            'https://mangadex.org/chapter/ecb8f061-0129-4fb6-b17a-eb87e3dd6a97',
            'https://mangadex.org/chapter/df133fee-3925-4f3b-89f8-4c5f087b655a',
            'https://mangadex.org/chapter/64c26ed4-d851-4fef-a576-09dc76ff2e49',
            'https://mangadex.org/chapter/0075acdf-06de-4fdc-a116-c3c8308b66ce',
            'https://mangadex.org/chapter/7a258eae-47c6-4fd2-b052-bf34d2143d57',
            'https://mangadex.org/chapter/47f12443-d711-4f28-9c11-9629bd31fb36'
        ])
