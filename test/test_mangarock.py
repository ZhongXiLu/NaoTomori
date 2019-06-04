
import unittest
from unittest.mock import MagicMock
from lxml import html

from naotomori.cogs.manga.mangarock import MangaRock


class TestMangaRock(unittest.TestCase):

    def setUp(self):
        self.mangarock = MangaRock()

    def test_findAnimeElements(self):
        """Test getting the manga html elements from a given mangarock html file"""

        with open('test/test_data/mangarock_1.html') as file:
            tree = html.fromstring(file.read())
            mangas = self.mangarock._findMangaElements(tree)
            self.assertEqual(len(mangas), 50)
            titles = []
            for manga in mangas:
                title = manga.xpath(".//a[contains(concat(' ', normalize-space(@class), ' '), ' _1A2Dc _3bzTG ')]")[0]
                titles.append(title.text_content())
            self.assertEqual(titles[:10], [
                'Wasteful Days of High School Girl',
                'Azur Lane 4-koma: Slow Ahead',
                'Beastars',
                'Naruto - Full Color',
                'Heavenly Match',
                'AKB49: Renai Kinshi Jourei',
                'Urara Meirochou',
                'Yancha Gal no Anjou-san',
                'Kaleido Star Comic Anthology',
                'Black Clover'
            ])

    def test_getRecentManga(self):
        """Test getting the most recent manga from the MangaRock homepage"""

        with open('test/test_data/mangarock_1.html') as file:
            tree = html.fromstring(file.read())
            mangas = self.mangarock._findMangaElements(tree)
            self.mangarock._findMangaElements = MagicMock(return_value=mangas)

        recentManga = self.mangarock.getRecent()
        self.assertEqual(len(recentManga), 16)
        self.assertEqual([manga.title for manga in recentManga], [
            'Wasteful Days of High School Girl',
            'Azur Lane 4-koma: Slow Ahead',
            'Beastars',
            'Naruto - Full Color',
            'Heavenly Match',
            'AKB49: Renai Kinshi Jourei',
            'Urara Meirochou',
            'Yancha Gal no Anjou-san',
            'Kaleido Star Comic Anthology',
            'Black Clover',
            'Boarding House Number 5',
            'The Promised Neverland',
            'With the Gods',
            'Utakata Dialogue',
            'Heart-Warming Meals with Mother Fenrir',
            'The Dark Seal'
        ])
        self.assertEqual([manga.progress for manga in recentManga], [
            'Vol.4 Chapter 56: Cavity',
            'Chapter 30',
            'Chapter 130: His Lead-Colored Prosthetic Leg is Sometimes Rainbow-Colored '
            'Under the Sun',
            'Vol.14 Chapter 126: Off Guard!!',
            'Chapter 135',
            'Vol.28 Chapter 247: Graduation Ceremony of Unrequited Love',
            'Vol.4 Chapter 27',
            'Vol.3 Chapter 40: A Slightly Upset Anjou-san',
            'Vol.1 Chapter 15: Amazing sea demon!',
            'Vol.20 Chapter 207: The Ultimate Magic',
            'Vol.1 Chapter 25',
            'Vol.TBD Chapter 136: Maze',
            'Chapter 52',
            'Vol.2 Chapter 10',
            'Chapter 2',
            'Chapter 5'
        ])
        self.assertEqual([manga.link for manga in recentManga], [
            'https://mangarock.com/manga/mrs-serie-100261862/chapter/mrs-chapter-200053040',
            'https://mangarock.com/manga/mrs-serie-100223631/chapter/mrs-chapter-200053026',
            'https://mangarock.com/manga/mrs-serie-100057603/chapter/mrs-chapter-200053019',
            'https://mangarock.com/manga/mrs-serie-174179/chapter/mrs-chapter-200053015',
            'https://mangarock.com/manga/mrs-serie-101212/chapter/mrs-chapter-200052967',
            'https://mangarock.com/manga/mrs-serie-9658/chapter/mrs-chapter-200052964',
            'https://mangarock.com/manga/mrs-serie-100080525/chapter/mrs-chapter-200052953',
            'https://mangarock.com/manga/mrs-serie-100325241/chapter/mrs-chapter-200052951',
            'https://mangarock.com/manga/mrs-serie-100308759/chapter/mrs-chapter-200052939',
            'https://mangarock.com/manga/mrs-serie-28856/chapter/mrs-chapter-200052846',
            'https://mangarock.com/manga/mrs-serie-100324887/chapter/mrs-chapter-200052925',
            'https://mangarock.com/manga/mrs-serie-303939/chapter/mrs-chapter-200052915',
            'https://mangarock.com/manga/mrs-serie-274067/chapter/mrs-chapter-200052888',
            'https://mangarock.com/manga/mrs-serie-100210465/chapter/mrs-chapter-200052886',
            'https://mangarock.com/manga/mrs-serie-200035959/chapter/mrs-chapter-200052883',
            'https://mangarock.com/manga/mrs-serie-200010386/chapter/mrs-chapter-200052877'
        ])
