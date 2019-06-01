
import unittest
import jikanpy
from unittest.mock import MagicMock
from discord.ext import commands

from tomorinao.cogs import usercog, animecog, mangacog


class TestUserCog(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the bot and User cog"""

        cls.bot = commands.Bot(command_prefix='!')
        cls.userCog = usercog.UserCog(cls.bot)
        cls.bot.add_cog(cls.userCog)
        cls.bot.add_cog(animecog.AnimeCog(cls.bot))
        cls.bot.add_cog(mangacog.MangaCog(cls.bot))

    def test_getMALProfile(self):
        """Test getting the MAL profile"""

        user = self.userCog._getMALProfile('DontKiIIMe')
        self.assertEqual(user['username'], 'DontKiIIMe')

        with self.assertRaises(jikanpy.exceptions.APIException):
            self.userCog._getMALProfile('jshfilusdfhiosefnhilsvuehf')

    def test_updateMALProfile(self):
        """Test updating the MAL profile, i.e. updating watching and reading list"""

        self.userCog.jikan.user = MagicMock(side_effect=[
            {
                'anime': [{
                    'mal_id': 38524,
                    'title': 'Shingeki no Kyojin Season 3 Part 2',
                    'image_url': 'https://cdn.myanimelist.net/images/anime/1517/100633.jpg?s=a00404552ef172c5cec8d586ed537214',
                }]
            },
            {
                'manga': [{
                    'mal_id': 103851,
                    'title': '5-toubun no Hanayome',
                    'image_url': 'https://cdn.myanimelist.net/images/manga/2/201572.jpg?s=c279b0d8a685d1c727b81ad88bac587f'
                }]
            }
        ])
        self.userCog.jikan.anime = MagicMock(side_effect=[{'title_english': 'Attack on Titan Season 3 Part 2'}])
        self.userCog.jikan.manga = MagicMock(side_effect=[{'title_english': 'The Quintessential Quintuplets'}])

        self.userCog._updateMALProfile('DontKiIIMe')

        self.assertEqual(self.bot.get_cog('AnimeCog').watching, [
            {
                'mal_id': 38524,
                'title': 'Shingeki no Kyojin Season 3 Part 2',
                'title_english': 'Attack on Titan Season 3 Part 2',
                'image_url': 'https://cdn.myanimelist.net/images/anime/1517/100633.jpg?s=a00404552ef172c5cec8d586ed537214',
            }
        ])
        self.assertEqual(self.bot.get_cog('MangaCog').reading, [
            {
                'mal_id': 103851,
                'title': '5-toubun no Hanayome',
                'title_english': 'The Quintessential Quintuplets',
                'image_url': 'https://cdn.myanimelist.net/images/manga/2/201572.jpg?s=c279b0d8a685d1c727b81ad88bac587f'
            }
        ])
