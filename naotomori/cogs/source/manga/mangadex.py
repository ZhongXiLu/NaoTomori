
import requests
from lxml import html

from naotomori.cogs.source.source import Source


class MangaDex:
    """
    MangaDex: provides a minimal MangaDex api.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.url = 'https://mangadex.org'

    def __str__(self):
        """
        String representation.

        :return: Name of source/api.
        """
        return "MangaDex"

    def _findMangaElements(self, tree):
        """
        Find all the manga elements in a html string.

        :param tree: The html string in form of a tree.
        :return: All the manga elements.
        """
        return tree.xpath('//div[@id="latest_update"]/div/*')

    def getRecent(self):
        """
        Get all the most recent manga chapters.

        :return: List of all the recent manga (Source objects) with the most recent ones at the front of the list.
        """
        mangas = []

        # Get all the manga html elements from the MangaRock homepage
        mangaElements = []
        with requests.Session() as session:
            session.headers = {'User-Agent': 'Mozilla/5.0'}
            session.cookies.set('mangadex_display_lang', '1')
            session.cookies.set('mangadex_filter_langs', '1')
            session.cookies.set('mangadex_theme', '1')
            response = session.get(self.url)
            if response.status_code == 200:
                tree = html.fromstring(response.text)
                mangaElements = self._findMangaElements(tree)

        # Construct the Manga objects
        for mangaElement in mangaElements:
            title = mangaElement.xpath(".//a[contains(concat(' ', normalize-space(@class), ' '), ' manga_title ')]")[0].text_content()
            ep = mangaElement.xpath(".//a[@class='text-truncate']")[0].text_content()
            link = mangaElement.xpath(".//a[@class='text-truncate']/@href")[0]
            if link.startswith('/'):
                # Relative path => prepend base url
                link = self.url + link
            mangas.append(Source(title=title, progress=ep, link=link))

        return mangas[:16]  # should be <= 16
