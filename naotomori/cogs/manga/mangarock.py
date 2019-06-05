
import requests
from lxml import html

from naotomori.cogs.source import Source


class MangaRock:
    """
    MangaRock: provides a minimal MangaRock api.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.url = 'https://mangarock.com'

    def __str__(self):
        """
        String representation.

        :return: Name of source/api.
        """
        return "MangaRock"

    def _findMangaElements(self, tree):
        """
        Find all the manga elements in a html string.

        :param tree: The html string in form of a tree.
        :return: All the manga elements.
        """
        return tree.xpath("//div[contains(concat(' ', normalize-space(@class), ' '), ' _1cii_ ')]")

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
            response = session.get(self.url)
            if response.status_code == 200:
                tree = html.fromstring(response.text)
                mangaElements = self._findMangaElements(tree)

        # Construct the Anime objects
        for mangaElement in mangaElements:
            # Get the title
            title = mangaElement.xpath(".//a[contains(concat(' ', normalize-space(@class), ' '), ' _1A2Dc _3bzTG ')]")[0].text_content()

            eps = []
            epElements = mangaElement.xpath(".//a[contains(concat(' ', normalize-space(@class), ' '), ' _1A2Dc _217pI ')]")
            del epElements[1::2]   # remove duplicates
            for epElement in epElements:
                eps.append(epElement.text_content())
            ep = "\n".join(eps)

            link = mangaElement.xpath(".//a[contains(concat(' ', normalize-space(@class), ' '), ' _1A2Dc _217pI ')]/@href")[0]
            if link.startswith('/'):
                # Relative path => prepend base url
                link = self.url + link
            mangas.append(Source(title=title, progress=ep, link=link))

        return mangas[:16]  # should be <= 16
