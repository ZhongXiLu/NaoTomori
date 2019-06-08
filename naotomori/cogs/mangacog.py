
from discord.ext import tasks, commands

from naotomori.cogs.source.manga.mangarock import MangaRock
from naotomori.cogs.sourcecog import SourceCog


class MangaCog(SourceCog):
    """
    MangaCog: extends the SourceCog.
    """

    def __init__(self, bot):
        """
        Constructor: initialize the cog.

        :param bot: The Discord bot.
        """
        super().__init__(bot)

        # Replace this with your own 'Manga API' if you want to use a different manga source
        self.source = MangaRock()

    @commands.command(brief='Set the manga source for retrieving new manga')
    async def setMangaSource(self, ctx, source: str):
        """
        Set the manga source, i.e. where it will retrieve the manga from.

        :param ctx: The context.
        :param source: Name of the manga source.
        """
        if source.lower() == "mangarock":
            self.source = MangaRock()
        else:
            await ctx.send('Unknown or unsupported manga source.')
            return
        self.list.clear()
        self.fillCache()
        await ctx.send(f'Successfully set the manga source to {source}.')

    @tasks.loop(minutes=5)
    async def checkNewLoop(self):
        """
        Loop that periodically calls checkNew to check for new manga.
        """
        await self.checkNew()
