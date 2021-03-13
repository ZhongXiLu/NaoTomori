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
        successful = self._setAnimeSource(source)
        if successful:
            self.bot.get_cog('DatabaseCog').updateValue("anime_source", source)
        if source.lower() == "none":
            self.list.clear()
            await ctx.send(f'Successfully removed the anime source.')
            return
        elif not successful:
            await ctx.send('Unknown or unsupported anime source.')
            return
        self.list.clear()
        self.fillCache()
        await ctx.send(f'Successfully set the anime source to {source}.')

    def _setAnimeSource(self, source):
        """
        Set the anime source, i.e. where it will retrieve the anime from.

        :param source: Name of the anime source.
        :return True if successful, False otherwise.
        """
        if source.lower() == "gogoanime":
            self.source = gogoanime.GoGoAnime()
        # elif source.lower() == "9anime":
        #     self.source = _9anime._9Anime()
        elif source.lower() == "none":
            self.source = None
        else:
            return False
        return True

    @commands.command(brief='Ignore an anime (don\'t send pings for a certain anime)')
    async def ignoreAnime(self, ctx, *args):
        """
        Ignore an anime.

        :param ctx: The context.
        :param args: Name of the anime.
        """
        await super(AnimeCog, self).ignore(ctx, True, *args)

    @commands.command(brief='Unignore an anime')
    async def unignoreAnime(self, ctx, *args):
        """
        Unignore an anime.

        :param ctx: The context.
        :param args: Name of the anime.
        """
        await super(AnimeCog, self).unignore(ctx, True, *args)

    @tasks.loop(minutes=5)
    async def checkNewLoop(self):
        """
        Loop that periodically calls checkNew to check for new anime.
        """
        await self.checkNew()
