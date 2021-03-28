import unittest
from unittest.mock import MagicMock
from lxml import html

from naotomori.cogs.source.manga.mangadex import MangaDex


class TestMangaDex(unittest.TestCase):
    """Tests for the MangaDex"""

    def setUp(self):
        self.mangadex = MangaDex()

    def test_findMangaElements(self):
        """Test getting the manga html elements from a given MangaDex html file"""

        with open('test/main/test_data/mangadex.html') as file:
            tree = html.fromstring(file.read())
            mangas = self.mangadex._findMangaElements(tree)
            self.assertEqual(len(mangas), 42)
            titles = []
            for manga in mangas:
                title = manga.xpath(".//a[contains(concat(' ', normalize-space(@class), ' '), ' manga_title ')]")[0]
                titles.append(title.text_content())
            self.assertEqual(titles[:10], [
                'Hana wa Junai ni Junjiru',
                'trash.',
                'Paradise Baby',
                'Kumo Desu ga, Nani ka? Daily Life of the Four Spider Sisters',
                'Kannou Shousetsuka no Neko',
                'Persona 5 Mementos Mission',
                'Metropolitan System',
                'Ouji Hiroimashita',
                'Honoo no Suna',
                'Enslave Lover'
            ])

    def test_getRecentManga(self):
        """Test getting the most recent manga from the MangaDex homepage"""

        with open('test/main/test_data/mangadex.html') as file:
            tree = html.fromstring(file.read())
            mangas = self.mangadex._findMangaElements(tree)
            self.mangadex._findMangaElements = MagicMock(return_value=mangas)

        recentManga = self.mangadex.getRecent()
        self.assertEqual(len(recentManga), 16)
        self.assertEqual([manga.title for manga in recentManga], [
            'Hana wa Junai ni Junjiru',
            'trash.',
            'Paradise Baby',
            'Kumo Desu ga, Nani ka? Daily Life of the Four Spider Sisters',
            'Kannou Shousetsuka no Neko',
            'Persona 5 Mementos Mission',
            'Metropolitan System',
            'Ouji Hiroimashita',
            'Honoo no Suna',
            'Enslave Lover',
            '2D Partner',
            'Nessa no Kusari',
            'Bliss~End Of Gods',
            'Shikanoko Nokonoko Koshitantan',
            'Koi no Myouyaku',
            'Sawatte, Tokashite'
        ])
        self.assertEqual([manga.progress for manga in recentManga], [
            'Vol. 1 Chapter 9.5',
            'Vol. 7 Chapter 51',
            'Vol. 1 Chapter 7.5',
            'Chapter 46',
            'Vol. 1 Chapter 2',
            'Vol. 1 Chapter 4.5',
            'Chapter 323',
            'Vol. 1 Chapter 7.5',
            'Vol. 1 Chapter 6.5',
            'Vol. 1 Chapter 7.5',
            'Chapter 16',
            'Vol. 1 Chapter 6.6',
            'Chapter 2',
            'Chapter 2',
            'Vol. 1 Chapter 4',
            'Vol. 1 Chapter 6.5'
        ])
        self.assertEqual([manga.link for manga in recentManga], [
            'https://mangadex.org/chapter/1002666',
            'https://mangadex.org/chapter/1002657',
            'https://mangadex.org/chapter/1002656',
            'https://mangadex.org/chapter/1002650',
            'https://mangadex.org/chapter/1002644',
            'https://mangadex.org/chapter/1002636',
            'https://mangadex.org/chapter/1002635',
            'https://mangadex.org/chapter/1002634',
            'https://mangadex.org/chapter/1002624',
            'https://mangadex.org/chapter/1002612',
            'https://mangadex.org/chapter/1002608',
            'https://mangadex.org/chapter/1002601',
            'https://mangadex.org/chapter/1002586',
            'https://mangadex.org/chapter/1002583',
            'https://mangadex.org/chapter/1002576',
            'https://mangadex.org/chapter/1002572'
        ])
