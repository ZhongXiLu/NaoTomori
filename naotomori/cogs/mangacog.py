from discord.ext import tasks, commands

from naotomori.cogs.source.manga.mangadex import MangaDex
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
        self.source = MangaDex()

    @commands.command(
        brief='Set the manga source for retrieving new manga (set source to "none" to remove the manga source)')
    async def setMangaSource(self, ctx, source: str):
        """
        Set the manga source, i.e. where it will retrieve the manga from.

        :param ctx: The context.
        :param source: Name of the manga source.
        """
        successful = self._setMangaSource(source)
        if successful:
            self.bot.get_cog('DatabaseCog').updateValue("manga_source", source)
        if source.lower() == "mangarock":
            await ctx.send(
                'Unfortunately MangaRock has removed all their reading features. Please use a different source.')
            return
        elif source.lower() == "none":
            self.list.clear()
            await ctx.send(f'Successfully removed the manga source.')
            return
        elif not successful:
            await ctx.send('Unknown or unsupported manga source.')
            return
        self.list.clear()
        self.fillCache()
        await ctx.send(f'Successfully set the manga source to {source}.')

    def _setMangaSource(self, source):
        """
        Set the manga source, i.e. where it will retrieve the manga from.

        :param source: Name of the manga source.
        :return True if successful, False otherwise.
        """
        if source.lower() == "mangadex":
            self.source = MangaDex()
        elif source.lower() == "none":
            self.source = None
        else:
            return False
        return True

    @commands.command(brief='Ignore a manga (don\'t send pings for a certain manga)')
    async def ignoreManga(self, ctx, *args):
        """
        Ignore a manga.

        :param ctx: The context.
        :param args: Name of the manga.
        """
        await super(MangaCog, self).ignore(ctx, False, *args)

    @commands.command(brief='Unignore a manga')
    async def unignoreManga(self, ctx, *args):
        """
        Unignore a manga.

        :param ctx: The context.
        :param args: Name of the manga.
        """
        await super(MangaCog, self).unignore(ctx, False, *args)

    @tasks.loop(minutes=5)
    async def checkNewLoop(self):
        """
        Loop that periodically calls checkNew to check for new manga.
        """
        await self.checkNew()
