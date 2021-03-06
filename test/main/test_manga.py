
import copy
import asynctest
from asyncio import Future
from unittest.mock import MagicMock
from discord.ext import commands
from lxml import html

from naotomori.cogs import mangacog
from naotomori.cogs.source.manga.mangarock import MangaRock


class TestMangaCog(asynctest.TestCase):
    """Tests for the MangaCog"""

    @classmethod
    def setUpClass(cls):
        """Set up the bot and Manga cog, as well as some premade manga elements"""

        cls.bot = commands.Bot(command_prefix='!')
        cls.mangaCog = mangacog.MangaCog(cls.bot)
        cls.mangaCog.source = MangaRock()
        cls.bot.add_cog(cls.mangaCog)

        with open('test/main/test_data/mangarock_1.html') as file:
            tree = html.fromstring(file.read())
            cls.mangas1 = cls.mangaCog.source._findMangaElements(tree)
        with open('test/main/test_data/mangarock_2.html') as file:
            tree = html.fromstring(file.read())
            cls.mangas2 = cls.mangaCog.source._findMangaElements(tree)

    def tearDown(self):
        self.mangaCog.cache = []

    def test_cacheManga(self):
        """Test the initial caching"""

        self.mangaCog.source._findMangaElements = MagicMock(return_value=self.mangas1)
        self.mangaCog.fillCache()
        self.assertEqual(len(self.mangaCog.cache), 16)
        self.assertEqual(list(self.mangaCog.cache), [
            'The Dark Seal',
            'Heart-Warming Meals with Mother Fenrir',
            'Utakata Dialogue',
            'With the Gods',
            'The Promised Neverland',
            'Boarding House Number 5',
            'Black Clover',
            'Kaleido Star Comic Anthology',
            'Yancha Gal no Anjou-san',
            'Urara Meirochou',
            'AKB49: Renai Kinshi Jourei',
            'Heavenly Match',
            'Naruto - Full Color',
            'Beastars',
            'Azur Lane 4-koma: Slow Ahead',
            'Wasteful Days of High School Girl'
        ])

    async def test_checkNewManga(self):
        """Test checking for new mangas and make sure 'pings' are sent out correctly"""

        self.mangaCog.source._findMangaElements = MagicMock(return_value=self.mangas1)
        self.mangaCog.fillCache()
        oldCache = copy.deepcopy(self.mangaCog.cache)
        self.assertEqual(len(self.mangaCog.cache), 16)

        # This allows mocking async methods, thanks to https://stackoverflow.com/a/46326234 :)
        f = Future()
        f.set_result(None)

        # User isn't watching anything => no pings are sent out
        self.mangaCog.sendPing = MagicMock(return_value=f)
        await self.mangaCog.checkNew()
        self.mangaCog.sendPing.assert_not_called()
        self.assertEqual(self.mangaCog.cache, oldCache)

        # User is reading '3-gatsu no Lion' => should receive one ping
        self.mangaCog.list.append({
            'mal_id': 1,
            'title': '3-gatsu no Lion',
            'title_english': 'March Comes in Like a Lion',
            'image_url': 'https://cdn.myanimelist.net/images/manga/1/52281.jpg'
        })
        self.mangaCog.source._findMangaElements = MagicMock(return_value=self.mangas2)    # has latest chapter of 3-gatsu no Lion
        oldCache = copy.deepcopy(self.mangaCog.cache)

        self.mangaCog.sendPing = MagicMock(return_value=f)
        await self.mangaCog.checkNew()
        self.assertEqual(self.mangaCog.sendPing.call_count, 1)
        self.mangaCog.sendPing.assert_called_once_with(
            '3-gatsu no Lion',
            'Vol.15 Chapter 159: Azusa Number 1 (4)',
            'https://mangarock.com/manga/mrs-serie-2048/chapter/mrs-chapter-200052839',
            'https://cdn.myanimelist.net/images/manga/1/52281.jpg'
        )
        self.assertNotEqual(self.mangaCog.cache, oldCache)
        self.assertTrue('3-gatsu no Lion' in self.mangaCog.cache)

    def test_setMangaSource(self):
        """Test setting a new manga source"""
        self.assertTrue(self.mangaCog._setMangaSource("mangadex"))
        self.assertEqual("MangaDex", str(self.mangaCog.source))
        self.assertTrue(self.mangaCog._setMangaSource("none"))
        self.assertIsNone(self.mangaCog.source)
        self.assertFalse(self.mangaCog._setMangaSource("mangarock"))
        self.assertFalse(self.mangaCog._setMangaSource("random source"))
