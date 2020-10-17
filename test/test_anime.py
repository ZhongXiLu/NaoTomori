
import copy
import asynctest
from asyncio import Future
from unittest.mock import MagicMock
from discord.ext import commands
from lxml import html

from naotomori.cogs import animecog
from naotomori.cogs.source.anime import _9anime


class TestAnimeCog(asynctest.TestCase):
    """Tests for the AnimeCog"""

    @classmethod
    def setUpClass(cls):
        """Set up the bot and Anime cog, as well as some premade anime elements"""

        cls.bot = commands.Bot(command_prefix='!')
        cls.animeCog = animecog.AnimeCog(cls.bot)
        cls.animeCog.source = _9anime._9Anime()
        cls.bot.add_cog(cls.animeCog)

        with open('test/test_data/9anime_1.html') as file:
            tree = html.fromstring(file.read())
            cls.animes1 = cls.animeCog.source._findAnimeElements(tree)
        with open('test/test_data/9anime_2.html') as file:
            tree = html.fromstring(file.read())
            cls.animes2 = cls.animeCog.source._findAnimeElements(tree)

    def tearDown(self):
        self.animeCog.cache = []

    def test_cacheAnime(self):
        """Test the initial caching"""

        self.animeCog.source._findAnimeElements = MagicMock(return_value=self.animes1)
        self.animeCog.fillCache()
        self.assertEqual(len(self.animeCog.cache), 14)
        self.assertEqual(list(self.animeCog.cache), [
            'Inu to Neko Docchi mo Katteru to Mainichi Tanoshii',
            'Pokemon (2019)',
            'Rebirth',
            'Strike Witches: Road to Berlin',
            'Kanojo, Okarishimasu (Dub)',
            'Hypnosis Mic: Division Rap Battle - Rhyme Anima',
            "King's Raid: Ishi wo Tsugumono-tachi",
            'Toaru Kagaku no Railgun T (Dub)',
            'Listeners (Dub)',
            'Dokyuu Hentai HxEros (Dub)',
            'Cardfight!! Vanguard Gaiden: If',
            'Enen no Shouboutai: Ni no Shou (Dub)',
            'Dragon Quest: Dai no Daibouken (2020)',
            'Haikyuu!!: To the Top 2nd Season'
        ])

    async def test_checkNewAnime(self):
        """Test checking for new animes and make sure 'pings' are sent out correctly"""

        self.animeCog.source._findAnimeElements = MagicMock(return_value=self.animes1)
        self.animeCog.fillCache()
        oldCache = copy.deepcopy(self.animeCog.cache)
        self.assertEqual(len(self.animeCog.cache), 14)

        # This allows mocking async methods, thanks to https://stackoverflow.com/a/46326234 :)
        f = Future()
        f.set_result(None)

        # User isn't watching anything => no pings are sent out
        self.animeCog.sendPing = MagicMock(return_value=f)
        await self.animeCog.checkNew()
        self.animeCog.sendPing.assert_not_called()
        self.assertEqual(self.animeCog.cache, oldCache)

        # User is watching 'The Journey of Elaina' => should receive one ping
        self.animeCog.list.append({
            'title': 'Majo no Tabitabi',
            'title_english': 'The Journey of Elaina',
            'image_url': 'https://cdn.myanimelist.net/images/anime/1802/108501.jpg'
        })
        self.animeCog.source._findAnimeElements = MagicMock(return_value=self.animes2)    # contains latest ep of Elaina
        oldCache = copy.deepcopy(self.animeCog.cache)

        self.animeCog.sendPing = MagicMock(return_value=f)
        await self.animeCog.checkNew()
        self.assertEqual(self.animeCog.sendPing.call_count, 1)
        self.animeCog.sendPing.assert_called_once_with(
            'Majo no Tabitabi',
            'Episode 3/12 ',
            'https://www12.9anime.ru/watch/the-journey-of-elaina.9vnn?ep=3',
            'https://cdn.myanimelist.net/images/anime/1802/108501.jpg'
        )
        self.assertNotEqual(self.animeCog.cache, oldCache)
        self.assertEqual(self.animeCog.cache[-1], 'Majo no Tabitabi')

