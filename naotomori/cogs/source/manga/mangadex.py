import json
import logging
from dataclasses import replace

import requests

from naotomori.cogs.source.source import Source

logger = logging.getLogger('NaoTomori')


class MangaDex:
    """
    MangaDex: provides a minimal MangaDex api.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.chapter_api = 'https://api.mangadex.org/chapter?limit=16&offset=0&translatedLanguage[]=en&order[publishAt]=desc'
        self.manga_api = 'https://api.mangadex.org/manga?&contentRating[]=safe&contentRating[]=suggestive&contentRating[]=erotica&contentRating[]=pornographic'
        self.chapter_url = 'https://mangadex.org/chapter/'

    def __str__(self):
        """
        String representation.

        :return: Name of source/api.
        """
        return "MangaDex"

    def _chaptersToSourceObjects(self, chapters):
        """
        Construct all the Source objects, given the json data for all the chapters.
        (json object from calling MangaDex's api)

        :param chapters: The json data for all the chapters.
        :return: All the Source objects.
        """
        source_map = {}     # chapter_id => Source object

        # Get the manga id and populate the source map + get the progress (chapter number)
        for chapter in chapters:
            chapter_id = chapter["data"]["id"]
            progress = None
            if chapter["data"]["attributes"]["chapter"]:
                progress = "Chapter " + chapter["data"]["attributes"]["chapter"]
            elif chapter["data"]["attributes"]["volume"]:
                progress = "Volume " + chapter["data"]["attributes"]["volume"]
            else:
                progress = "Oneshot"
            for relationship in chapter["relationships"]:
                if relationship["type"] == "manga":
                    manga_id = relationship["id"]
                    source = Source("", progress, self.chapter_url + chapter_id)
                    if manga_id not in source_map:
                        # fill other fields in later
                        source_map[manga_id] = [source]
                    else:
                        # another chapter from the same manga
                        source_map[manga_id].append(source)

        # Get the manga name
        manga_url_with_params = self.manga_api
        for manga_id in source_map.keys():
            manga_url_with_params += "&ids[]=" + manga_id
        manga_url_with_params += "&limit=" + str(len(source_map.keys()))
        with requests.Session() as session:
            response = session.get(manga_url_with_params)
            if response.status_code == 200:
                mangas = json.loads(response.text)["results"]
                for manga in mangas:
                    manga_id = manga["data"]["id"]
                    title = manga["data"]["attributes"]["title"]["en"]
                    new_sources = []
                    sources = source_map[manga_id]
                    for source in sources:
                        new_source = replace(source, title=title)
                        new_sources.append(new_source)
                    new_sources.reverse()  # reverse to put newest first in list
                    source_map[manga_id] = new_sources
            else:
                logger.error(f"Received {response.status_code} from {str(self)}")

        return [source for sublist in list(source_map.values()) for source in sublist]

    def getRecent(self):
        """
        Get all the most recent manga chapters.

        :return: List of all the recent manga (Source objects) with the most recent ones at the front of the list.
        """

        # Call MangaDex's api to retrieve the latest manga chapters
        with requests.Session() as session:
            response = session.get(self.chapter_api)
            if response.status_code == 200:
                chapters = json.loads(response.text)["results"]
                return self._chaptersToSourceObjects(chapters)[:16]     # should be <= 16
            else:
                logger.error(f"Received {response.status_code} from {str(self)}")
                return []
