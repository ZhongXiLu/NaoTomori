import discord
import logging
from discord.ext import commands

from naotomori.cogs import usercog, animecog, mangacog, databasecog

logger = logging.getLogger('NaoTomori')


class NaoTomori(commands.Bot):
    """
    NaoTomori: Discord bot.
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor: initialize the bot and add all the cogs.
        """
        logger.info("Initializing bot")
        self.started = False
        super().__init__(*args, **kwargs)

        logger.info("Adding cogs to bot")
        self.add_cog(usercog.UserCog(self))
        self.add_cog(animecog.AnimeCog(self))
        self.add_cog(mangacog.MangaCog(self))
        self.add_cog(databasecog.DatabaseCog(self))

    async def on_ready(self):
        """
        Called when the bot is 'ready'; start all the cogs.
        """
        await self.change_presence(activity=discord.Game(name="Setting up"))
        if not self.started:
            logger.info("Starting all the cogs")
            self.started = True
            self.get_cog('DatabaseCog').start()
            self.get_cog('AnimeCog').start()
            self.get_cog('MangaCog').start()
            self.get_cog('UserCog').start()

        logger.info(f"Logged in as {self.user.name}")
        await self.change_presence(activity=discord.Game(name="Running!"))
