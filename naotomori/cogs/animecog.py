from discord.ext import tasks, commands

from naotomori.cogs.source.anime import _9anime, gogoanime
from naotomori.cogs.sourcecog import SourceCog


class AnimeCog(SourceCog):
    """
    AnimeCog: extends the SourceCog.
    """

    def __init__(self, bot):
        """
        Constructor: initialize the cog.

        :param bot: The Discord bot.
        """
        super().__init__(bot)

        # Replace this with your own 'Anime API' if you want to use a different anime source
        # self.source = _9anime._9Anime()
        self.source = gogoanime.GoGoAnime()

    @commands.command(
        brief='Set the anime source for retrieving new anime (set source to "none" to remove the anime source)')
    async def setAnimeSource(self, ctx, source: str):
        """
        Set the anime source, i.e. where it will retrieve the anime from.

        :param ctx: The context.
        :param source: Name of the anime source.
        """
        if source.lower() == "gogoanime":
            self.source = gogoanime.GoGoAnime()
        elif source.lower() == "9anime":
            self.source = _9anime._9Anime()
        elif source.lower() == "none":
            self.source = None
            self.list.clear()
            await ctx.send(f'Successfully removed the anime source.')
            return
        else:
            await ctx.send('Unknown or unsupported anime source.')
            return
        self.list.clear()
        self.fillCache()
        await ctx.send(f'Successfully set the anime source to {source}.')

    @tasks.loop(minutes=5)
    async def checkNewLoop(self):
        """
        Loop that periodically calls checkNew to check for new anime.
        """
        await self.checkNew()
