
import unittest
from unittest.mock import MagicMock
from lxml import html

from naotomori.cogs.anime._9anime import _9Anime


class Test9Anime(unittest.TestCase):

    def setUp(self):
        self._9anime = _9Anime()

    def test_findAnimeElements(self):
        """Test getting the anime html elements from a given 9anime html file"""

        with open('test/test_data/9anime_1.html') as file:
            tree = html.fromstring(file.read())
            animes = self._9anime._findAnimeElements(tree)
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

    def test_getRecentAnime(self):
        """Test getting the most recent anime from the 9anime homepage"""

        with open('test/test_data/9anime_1.html') as file:
            tree = html.fromstring(file.read())
            animes = self._9anime._findAnimeElements(tree)
            self._9anime._findAnimeElements = MagicMock(return_value=animes)

        recentAnime = self._9anime.getRecentAnime()
        self.assertEqual(len(recentAnime), 15)
        self.assertEqual([anime.title for anime in recentAnime], [
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
        self.assertEqual([anime.ep for anime in recentAnime], [
            ' Ep 8/24 ',
            ' Ep 9/11 ',
            ' Ep 32/36 ',
            ' Ep 16 ',
            ' Ep 8/12 ',
            ' Ep 6/12 ',
            ' Ep 8/12 ',
            ' Ep 19/25 ',
            ' Ep 8/12 ',
            ' Ep 21/25 ',
            ' Ep 104 ',
            ' Ep 7/12 ',
            ' Ep 4/12 ',
            ' Ep 68 ',
            ' Ep 7/26 '
        ])
        self.assertEqual([anime.link for anime in recentAnime], [
            'https://www1.9anime.nl/watch/carole-tuesday.18vq',
            'https://www1.9anime.nl/watch/operation-han-gyaku-sei-million-arthur-2nd-season.3nj2',
            'https://www1.9anime.nl/watch/le-cirque-de-karakuri.46xx',
            'https://www1.9anime.nl/watch/fight-league-gear-gadget-generators.qw65',
            'https://www1.9anime.nl/watch/kenja-no-mago-dub.k5o9',
            'https://www1.9anime.nl/watch/sewayaki-kitsune-no-senko-san-dub.nl38',
            'https://www1.9anime.nl/watch/kenja-no-mago.40wx',
            'https://www1.9anime.nl/watch/the-rising-of-the-shield-hero-dub.rxxy',
            'https://www1.9anime.nl/watch/sewayaki-kitsune-no-senko-san.pv2x',
            'https://www1.9anime.nl/watch/the-rising-of-the-shield-hero.6kl0',
            'https://www1.9anime.nl/watch/yu-gi-oh-vrains.r8mp',
            'https://www1.9anime.nl/watch/xia-gan-yi-dan-shen-jianxin.om98',
            'https://www1.9anime.nl/watch/mitsuboshi-colors-dub.wxo4',
            'https://www1.9anime.nl/watch/shinkansen-henkei-robo-shinkalion-the-animation.15zq',
            'https://www1.9anime.nl/watch/yu-no-a-girl-who-chants-love-at-the-bound-of-this-world-dub.vwn4'
        ])
