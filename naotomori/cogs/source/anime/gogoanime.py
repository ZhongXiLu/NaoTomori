
import requests
from lxml import html

from naotomori.cogs.source.source import Source


class GoGoAnime:
    """
    GoGoAnime: provides a minimal GoGoAnime api.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.url = 'https://gogoanime.so/'

    def __str__(self):
        """
        String representation.

        :return: Name of source/api.
        """
        return "GoGoAnime"

    def _findAnimeElements(self, tree):
        """
        Find all the anime elements in a html string.

        :param tree: The html string in form of a tree.
        :return: All the anime elements.
        """
        return tree.xpath("//ul[contains(concat(' ', normalize-space(@class), ' '), ' items ')]/*")

    def getRecent(self):
        """
        Get all the most recent anime chapters.

        :return: List of all the recent anime (Source objects) with the most recent ones at the front of the list.
        """
        animes = []

        # Get all the anime html elements from the GoGoAnime homepage
        animeElements = []
        with requests.Session() as session:
            session.headers = {'User-Agent': 'Mozilla/5.0'}
            response = session.get(self.url)
            if response.status_code == 200:
                tree = html.fromstring(response.text)
                # Get all the recent anime's
                animeElements = self._findAnimeElements(tree)

        # Construct the Anime objects
        for animeElement in animeElements:
            title = animeElement.xpath(".//p/a[@title]")[0].text_content()
            link = animeElement.xpath(".//p/a[@title]/@href")[0]
            if link.startswith('/'):
                # Relative path => prepend base url
                link = self.url + link
            ep = animeElement.xpath(".//p[contains(concat(' ', normalize-space(@class), ' '), ' episode ')]")[0].text_content()
            animes.append(Source(title=title, progress=ep, link=link))

        return animes[:16]  # should be <= 16
