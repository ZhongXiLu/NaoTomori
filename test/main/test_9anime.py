
import unittest
from unittest.mock import MagicMock, patch

import lxml
import requests
from lxml import html

from naotomori.cogs.source.anime._9anime import _9Anime


class Test9Anime(unittest.TestCase):
    """Tests for _9Anime"""

    def setUp(self):
        self._9anime = _9Anime()
        with open('test/main/test_data/9anime_2.html') as file:
            tree = html.fromstring(file.read())
            self.animes = self._9anime._findAnimeElements(tree)

    def test_findAnimeElements(self):
        """Test getting the anime html elements from a given 9anime html file"""

        self.assertEqual(len(self.animes), 15)
        titles = []
        for anime in self.animes:
            query = anime.xpath(".//@data-jtitle")
            title = query[0] if len(query) > 0 else None
            if title:
                titles.append(title)
        self.assertEqual(len(titles), 15)
        self.assertEqual(titles, [
            'Majo no Tabitabi',
            'Haikyuu!!: To the Top 2nd Season',
            'Dragon Quest: Dai no Daibouken (2020)',
            'Enen no Shouboutai: Ni no Shou (Dub)',
            'Cardfight!! Vanguard Gaiden: If',
            'Dokyuu Hentai HxEros (Dub)',
            'Listeners (Dub)',
            'Toaru Kagaku no Railgun T (Dub)',
            "King's Raid: Ishi wo Tsugumono-tachi",
            'Hypnosis Mic: Division Rap Battle - Rhyme Anima',
            'Kanojo, Okarishimasu (Dub)',
            'Strike Witches: Road to Berlin',
            'Rebirth',
            'Pokemon (2019)',
            'Inu to Neko Docchi mo Katteru to Mainichi Tanoshii'
        ])

    @patch.object(requests.Session, 'get')
    @patch.object(lxml.html, 'fromstring')
    def test_getRecentAnime(self, html_fromstring, mock_session):
        """Test getting the most recent anime from the 9anime homepage"""

        self._9anime._findAnimeElements = MagicMock(return_value=self.animes)
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_session.return_value = mock_response
        html_fromstring.return_value = ""

        recentAnime = self._9anime.getRecent()
        self.assertEqual(len(recentAnime), 15)
        self.assertEqual([anime.title for anime in recentAnime], [
            'Majo no Tabitabi',
            'Haikyuu!!: To the Top 2nd Season',
            'Dragon Quest: Dai no Daibouken (2020)',
            'Enen no Shouboutai: Ni no Shou (Dub)',
            'Cardfight!! Vanguard Gaiden: If',
            'Dokyuu Hentai HxEros (Dub)',
            'Listeners (Dub)',
            'Toaru Kagaku no Railgun T (Dub)',
            "King's Raid: Ishi wo Tsugumono-tachi",
            'Hypnosis Mic: Division Rap Battle - Rhyme Anima',
            'Kanojo, Okarishimasu (Dub)',
            'Strike Witches: Road to Berlin',
            'Rebirth',
            'Pokemon (2019)',
            'Inu to Neko Docchi mo Katteru to Mainichi Tanoshii'
        ])
        self.assertEqual([anime.progress for anime in recentAnime], [
            'Episode 3/12 ',
            'Episode 3/12 ',
            'Episode 3 ',
            'Episode 10/24 ',
            'Episode 19 ',
            'Episode 7/12 ',
            'Episode 2/12 ',
            'Episode 23/25 ',
            'Episode 3/26 ',
            'Episode 3/13 ',
            'Episode 8/12 ',
            'Episode 2/12 ',
            'Episode 26 ',
            'Episode 41 ',
            'Episode 3 '
        ])
        self.assertEqual([anime.link for anime in recentAnime], [
            'https://www12.9anime.ru/watch/the-journey-of-elaina.9vnn?ep=3',
            'https://www12.9anime.ru/watch/haikyuu-to-the-top-2nd-season.nyn8?ep=3',
            'https://www12.9anime.ru/watch/dragon-quest-dai-no-daibouken-2020.j4rn?ep=3',
            'https://www12.9anime.ru/watch/enen-no-shouboutai-ni-no-shou-dub.yl7p?ep=10',
            'https://www12.9anime.ru/watch/cardfight-vanguard-gaiden-if.76yy?ep=19',
            'https://www12.9anime.ru/watch/super-hxeros-dub.05mk?ep=7',
            'https://www12.9anime.ru/watch/listeners-dub.543v?ep=2',
            'https://www12.9anime.ru/watch/a-certain-scientific-railgun-t-dub.lwln?ep=23',
            'https://www12.9anime.ru/watch/kings-raid-ishi-wo-tsugumono-tachi.oz5z?ep=3',
            'https://www12.9anime.ru/watch/hypnosis-mic-division-rap-battle-rhyme-anima.9p20?ep=3',
            'https://www12.9anime.ru/watch/rent-a-girlfriend-dub.9pj0?ep=8',
            'https://www12.9anime.ru/watch/strike-witches-road-to-berlin.0lxr?ep=2',
            'https://www12.9anime.ru/watch/rebirth.0j57?ep=26',
            'https://www12.9anime.ru/watch/pokemon-journeys-the-series.3m68?ep=41',
            'https://www12.9anime.ru/watch/with-a-dog-and-a-cat-every-day-is-fun.jxj2?ep=3'
        ])
