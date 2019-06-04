
import unittest
from unittest.mock import MagicMock
from lxml import html

from naotomori.cogs.anime.gogoanime import GoGoAnime


class TestGoGoAnime(unittest.TestCase):

    def setUp(self):
        self.gogoanime = GoGoAnime()

    def test_findAnimeElements(self):
        """Test getting the anime html elements from a given GoGoAnime html file"""

        with open('test/test_data/gogoanime.html') as file:
            tree = html.fromstring(file.read())
            animes = self.gogoanime._findAnimeElements(tree)
            self.assertEqual(len(animes), 20)
            titles = []
            for anime in animes:
                title = anime.xpath(".//p/a[@title]")
                titles.append(title[0].text_content())
            self.assertEqual(len(titles), 20)
            self.assertEqual(titles[:10], [
                'Detective Conan',
                'Mix: Meisei Story',
                'Jewelpet Sunshine',
                'Qin Shi Ming Yue: Kong Shan Niao Yu',
                'Whited Nighttime',
                'Shao Nian Ge Xing',
                'Fruits Basket (2019)',
                'Hitoribocchi no OO Seikatsu',
                'Midara na Ao-chan wa Benkyou ga Dekinai',
                'Senryuu Shoujo'
            ])

    def test_getRecentAnime(self):
        """Test getting the most recent anime from the GoGoAnime homepage"""

        with open('test/test_data/gogoanime.html') as file:
            tree = html.fromstring(file.read())
            animes = self.gogoanime._findAnimeElements(tree)
            self.gogoanime._findAnimeElements = MagicMock(return_value=animes)

        recentAnime = self.gogoanime.getRecent()
        self.assertEqual(len(recentAnime), 16)
        self.assertEqual([anime.title for anime in recentAnime[:10]], [
            'Detective Conan',
            'Mix: Meisei Story',
            'Jewelpet Sunshine',
            'Qin Shi Ming Yue: Kong Shan Niao Yu',
            'Whited Nighttime',
            'Shao Nian Ge Xing',
            'Fruits Basket (2019)',
            'Hitoribocchi no OO Seikatsu',
            'Midara na Ao-chan wa Benkyou ga Dekinai',
            'Senryuu Shoujo'
        ])
        self.assertEqual([anime.progress for anime in recentAnime[:10]], [
            'Episode 941',
            'Episode 9',
            'Episode 34',
            'Episode 3',
            'Episode 22',
            'Episode 25',
            'Episode 9',
            'Episode 9',
            'Episode 9',
            'Episode 9'
        ])
        self.assertEqual([anime.link for anime in recentAnime[:10]], [
            'https://www4.gogoanime.io/detective-conan-episode-941',
            'https://www4.gogoanime.io/mix-meisei-story-episode-9',
            'https://www4.gogoanime.io/jewelpet-sunshine-episode-34',
            'https://www4.gogoanime.io/qin-shi-ming-yue-kong-shan-niao-yu-episode-3',
            'https://www4.gogoanime.io/whited-nighttime-episode-22',
            'https://www4.gogoanime.io/shao-nian-ge-xing-episode-25',
            'https://www4.gogoanime.io/fruits-basket-2019-episode-9',
            'https://www4.gogoanime.io/hitoribocchi-no-oo-seikatsu-episode-9',
            'https://www4.gogoanime.io/midara-na-ao-chan-wa-benkyou-ga-dekinai-episode-9',
            'https://www4.gogoanime.io/senryuu-shoujo-episode-9'
        ])
