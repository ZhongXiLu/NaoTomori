import unittest
from naotomori.cogs.source.anime._9anime import _9Anime
from naotomori.cogs.source.anime.gogoanime import GoGoAnime
from naotomori.cogs.source.manga.mangadex import MangaDex
from naotomori.cogs.source.manga.mangarock import MangaRock


class TestApi(unittest.TestCase):
    """Tests for the 3rd party api's"""

    @unittest.skip("Cant easily scrape their website :thinking:")
    def test_9anime(self):
        """Test 9Anime api"""

        _9anime = _9Anime()
        animes = _9anime.getRecent()
        self.assertTrue(len(animes) > 0)

    def test_gogoanime(self):
        """Test GoGoAnime api"""

        gogoanime = GoGoAnime()
        animes = gogoanime.getRecent()
        self.assertTrue(len(animes) > 0)

    def test_mangadex(self):
        """Test MangaDex api"""

        mangadex = MangaDex()
        mangas = mangadex.getRecent()
        self.assertTrue(len(mangas) > 0)

    @unittest.skip("MangaRock discontinued their services")
    def test_mangarock(self):
        """Test MangaRock api"""

        mangarock = MangaRock()
        mangas = mangarock.getRecent()
        self.assertTrue(len(mangas) > 0)
