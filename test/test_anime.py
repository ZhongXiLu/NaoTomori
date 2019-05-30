
import asynctest
from asyncio import Future
from unittest.mock import MagicMock

from discord.ext import commands
from lxml import html

from TomoriNao import anime


class TestUserCache(asynctest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the bot and Anime cog, as well as some premade anime elements"""

        cls.bot = commands.Bot(command_prefix='!')
        cls.anime = anime.Anime(cls.bot)
        cls.bot.add_cog(cls.anime)

        with open('test_data/9anime_1.html') as file:
            tree = html.fromstring(file.read())
            cls.animes1 = cls.anime.findAnimeElements(tree)
        with open('test_data/9anime_2.html') as file:
            tree = html.fromstring(file.read())
            cls.animes2 = cls.anime.findAnimeElements(tree)

    def test_findAnime(self):
        """Test finding the anime elements on a 9anime html page"""

        with open('test_data/9anime_1.html') as file:
            tree = html.fromstring(file.read())
            animes = self.anime.findAnimeElements(tree)
            self.assertEqual(len(animes), 23)
            titles = []
            for anime in animes:
                query = anime.xpath(
                    "*[1]/a[contains(concat(' ', normalize-space(@class), ' '), ' name ')]/@data-jtitle")
                title = query[0] if len(query) > 0 else None
                if title:
                    titles.append(title)
            self.assertEqual(len(titles), 15)
            self.assertEqual(titles, [
                'Carole & Tuesday',
                'Hangyakusei Million Arthur 2nd Season',
                'Karakuri Circus',
                'Fight League: Gear Gadget Generators',
                'Kenja no Mago (Dub)',
                'Sewayaki Kitsune no Senko-san (Dub)',
                'Kenja no Mago',
                'Tate no Yuusha no Nariagari (Dub)',
                'Sewayaki Kitsune no Senko-san',
                'Tate no Yuusha no Nariagari',
                'Yu☆Gi☆Oh! VRAINS',
                'Xia Gan Yi Dan Shen Jianxin',
                'Mitsuboshi Colors (Dub)',
                'Shinkansen Henkei Robo Shinkalion The Animation',
                'Kono Yo no Hate de Koi wo Utau Shoujo YU-NO (Dub)'
            ])

    def test_cacheAnime(self):
        """Test the initial caching"""

        self.anime.getRecentAnime = MagicMock(return_value=self.animes1)
        self.anime.cacheAnime()
        self.assertEqual(len(self.anime.cachedAnimes), 8)
        self.assertEqual(self.anime.cachedAnimes, [
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

        self.anime.getRecentAnime = MagicMock(return_value=self.animes1)
        self.anime.cacheAnime()
        self.assertEqual(len(self.anime.cachedAnimes), 8)

        # This allows mocking async methods, thanks to https://stackoverflow.com/a/46326234 :)
        f = Future()
        f.set_result(None)

        # User isn't watching anything => no pings are sent out
        self.anime.sendPing = MagicMock(return_value=f)
        await self.anime.checkNewAnime()
        self.anime.sendPing.assert_not_called()

        # User is watching 'One Punch Man 2nd Season' => should receive one ping
        self.anime.watching.append({
            'title': 'One Punch Man 2nd Season',
            'image_url': 'https://cdn.myanimelist.net/images/anime/1805/99571.jpg?s=76893d6eb26f8add6731bcfa56f243ec'
        })
        self.anime.getRecentAnime = MagicMock(return_value=self.animes2)    # has latest ep of OPM S2

        self.anime.sendPing = MagicMock(return_value=f)
        await self.anime.checkNewAnime()
        self.assertEqual(self.anime.sendPing.call_count, 1)
        self.anime.sendPing.assert_called_once_with(
            'One Punch Man 2nd Season',
            ' Ep 8/12',
            'https://www1.9anime.nl/watch/one-punch-man-2nd-season.qqmj',
            'https://cdn.myanimelist.net/images/anime/1805/99571.jpg?s=76893d6eb26f8add6731bcfa56f243ec'
        )
