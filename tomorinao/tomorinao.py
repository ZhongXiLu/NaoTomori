
import discord
from discord.ext import commands

from tomorinao.cogs import user, anime


class TomoriNao(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_cog(user.User(self))
        self.add_cog(anime.Anime(self))

    async def on_ready(self):
        print(f"Logged in as {self.user.name}")
        await self.change_presence(activity=discord.Game(name="Running!"))
        self.get_cog('Anime').fillCache()
