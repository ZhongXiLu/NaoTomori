
from dataclasses import dataclass


@dataclass
class Source:
    """
    Source: dataclass to store information for an anime/manga.
    """

    title: str      # The title
    progress: str   # The progress (e.g. Episode 8/12)
    link: str       # Link to the anime/manga
