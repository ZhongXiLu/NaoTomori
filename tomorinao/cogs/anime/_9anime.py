
import requests
from lxml import html

from .anime import Anime


class _9Anime:

    def __init__(self):
        self.url = 'https://www1.9anime.nl/home'

    def _findAnimeElements(self, tree):
        return tree.xpath("//div[contains(concat(' ', normalize-space(@class), ' '), ' content ')\
                                            and not(contains(concat(' ', @class, ' '), ' hidden '))]/*[1]/*[1]/*")

    # Return the most recent animes (should be less than 16) with the most recent at the front of the list
    def getRecentAnime(self):
        animes = []

        # Get all the anime html elements from the 9anime homepage
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
            # Get the title
            query = animeElement.xpath(
                "*[1]/a[contains(concat(' ', normalize-space(@class), ' '), ' name ')]/@data-jtitle")
            title = query[0] if len(query) > 0 else None
            if title:
                ep = animeElement.xpath(".//div[contains(concat(' ', normalize-space(@class), ' '), ' ep ')]")[0].text_content()
                link = animeElement.xpath("*[1]/a[contains(concat(' ', normalize-space(@class), ' '), ' name ')]/@href")[0]
                animes.append(Anime(title=title, ep=ep, link=link))

        return animes
