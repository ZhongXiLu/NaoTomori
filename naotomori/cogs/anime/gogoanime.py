
import requests
from lxml import html

from naotomori.cogs.source import Source


class GoGoAnime:

    def __init__(self):
        self.url = 'https://www4.gogoanime.io/'

    def __str__(self):
        return "GoGoAnime"

    def _findAnimeElements(self, tree):
        return tree.xpath("//ul[contains(concat(' ', normalize-space(@class), ' '), ' items ')]/*")

    # Return the most recent animes (should be less than 16) with the most recent at the front of the list
    def getRecent(self):
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

        return animes[:16]
