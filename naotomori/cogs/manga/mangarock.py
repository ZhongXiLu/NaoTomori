
import requests
from lxml import html

from .manga import Manga


class MangaRock:

    def __init__(self):
        self.url = 'https://mangarock.com'

    def __str__(self):
        return "MangaRock"

    def _findMangaElements(self, tree):
        return tree.xpath("//div[contains(concat(' ', normalize-space(@class), ' '), ' _1cii_ ')]")

    # Return the most recent manga chapters (should be less than 16) with the most recent at the front of the list
    def getRecent(self):
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
        for mangaElements in mangaElements:
            # Get the title
            title = mangaElements.xpath(".//a[contains(concat(' ', normalize-space(@class), ' '), ' _1A2Dc _3bzTG ')]")[0].text_content()
            ep = mangaElements.xpath(".//a[contains(concat(' ', normalize-space(@class), ' '), ' _1A2Dc _217pI ')]")[0].text_content()
            link = mangaElements.xpath(".//a[contains(concat(' ', normalize-space(@class), ' '), ' _1A2Dc _217pI ')]/@href")[0]
            if link.startswith('/'):
                # Relative path => prepend base url
                link = self.url + link
            mangas.append(Manga(title=title, ep=ep, link=link))

        return mangas[:16]
