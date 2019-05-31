
import copy
import asynctest
from asyncio import Future
from unittest.mock import MagicMock
from discord.ext import commands
from lxml import html

from tomorinao.cogs import animecog


class TestAnimeCog(asynctest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the bot and Anime cog, as well as some premade anime elements"""

        cls.bot = commands.Bot(command_prefix='!')
        cls.animeCog = animecog.AnimeCog(cls.bot)
        cls.bot.add_cog(cls.animeCog)

        with open('test/test_data/9anime_1.html') as file:
            tree = html.fromstring(file.read())
            cls.animes1 = cls.animeCog.anime._findAnimeElements(tree)
        with open('test/test_data/9anime_2.html') as file:
            tree = html.fromstring(file.read())
            cls.animes2 = cls.animeCog.anime._findAnimeElements(tree)

    def tearDown(self):
        self.animeCog.cachedAnimes = []

    def test_cacheAnime(self):
        """Test the initial caching"""

        self.animeCog.anime._findAnimeElements = MagicMock(return_value=self.animes1)
        self.animeCog.fillCache()
        self.assertEqual(len(self.animeCog.cachedAnimes), 15)
        self.assertEqual(self.animeCog.cachedAnimes, [
            'Kono Yo no Hate de Koi wo Utau Shoujo YU-NO (Dub)',
            'Shinkansen Henkei Robo Shinkalion The Animation',
            'Mitsuboshi Colors (Dub)',
            'Xia Gan Yi Dan Shen Jianxin',
            'Yu☆Gi☆Oh! VRAINS',
            'Tate no Yuusha no Nariagari',
            'Sewayaki Kitsune no Senko-san',
            'Tate no Yuusha no Nariagari (Dub)',
            'Kenja no Mago',
            'Sewayaki Kitsune no Senko-san (Dub)',
            'Kenja no Mago (Dub)',
            'Fight League: Gear Gadget Generators',
            'Karakuri Circus',
            'Hangyakusei Million Arthur 2nd Season',
            'Carole & Tuesday'
        ])

    async def test_checkNewAnime(self):
        """Test checking for new animes and make sure 'pings' are sent out correctly"""

        self.animeCog.anime._findAnimeElements = MagicMock(return_value=self.animes1)
        self.animeCog.fillCache()
        oldCache = copy.deepcopy(self.animeCog.cachedAnimes)
        self.assertEqual(len(self.animeCog.cachedAnimes), 15)

        # This allows mocking async methods, thanks to https://stackoverflow.com/a/46326234 :)
        f = Future()
        f.set_result(None)

        # User isn't watching anything => no pings are sent out
        self.animeCog.sendPing = MagicMock(return_value=f)
        await self.animeCog.checkNewAnime()
        self.animeCog.sendPing.assert_not_called()
        self.assertEqual(self.animeCog.cachedAnimes, oldCache)

        # User is watching 'One Punch Man 2nd Season' => should receive one ping
        self.animeCog.watching.append({
            'title': 'One Punch Man 2nd Season',
            'title_english': 'One Punch-Man 2',
            'image_url': 'https://cdn.myanimelist.net/images/anime/1805/99571.jpg?s=76893d6eb26f8add6731bcfa56f243ec'
        })
        self.animeCog.anime._findAnimeElements = MagicMock(return_value=self.animes2)    # has latest ep of OPM S2
        oldCache = copy.deepcopy(self.animeCog.cachedAnimes)

        self.animeCog.sendPing = MagicMock(return_value=f)
        await self.animeCog.checkNewAnime()
        self.assertEqual(self.animeCog.sendPing.call_count, 1)
        self.animeCog.sendPing.assert_called_once_with(
            'One Punch Man 2nd Season',
            ' Ep 8/12',
            'https://www1.9anime.nl/watch/one-punch-man-2nd-season.qqmj',
            'https://cdn.myanimelist.net/images/anime/1805/99571.jpg?s=76893d6eb26f8add6731bcfa56f243ec'
        )
        self.assertNotEqual(self.animeCog.cachedAnimes, oldCache)
        self.assertEqual(self.animeCog.cachedAnimes[-1], 'One Punch Man 2nd Season')

