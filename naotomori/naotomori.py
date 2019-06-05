
import discord
from discord.ext import commands

from naotomori.cogs import usercog, animecog, mangacog, databasecog


class NaoTomori(commands.Bot):
    """
    NaoTomori: Discord bot.
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor: initialize the bot and add all the cogs.
        """
        super().__init__(*args, **kwargs)
        self.add_cog(usercog.UserCog(self))
        self.add_cog(animecog.AnimeCog(self))
        self.add_cog(mangacog.MangaCog(self))
        self.add_cog(databasecog.DatabaseCog(self))

    async def on_ready(self):
        """
        Called when the bot is 'ready', starts all the attached cogs.
        """
        print(f"Logged in as {self.user.name}")
        await self.change_presence(activity=discord.Game(name="Running!"))
        self.get_cog('DatabaseCog').start()
        self.get_cog('AnimeCog').start()
        self.get_cog('MangaCog').start()
        self.get_cog('UserCog').start()
