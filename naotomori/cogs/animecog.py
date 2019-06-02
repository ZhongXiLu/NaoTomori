
from discord.ext import tasks, commands

from naotomori.cogs.anime import _9anime, gogoanime
from naotomori.cogs.source import SourceCog


class AnimeCog(SourceCog):

    def __init__(self, bot):
        super().__init__(bot)

        # Replace this with your own 'Anime API' if you want to use a different anime source
        # self.anime = _9anime._9Anime()
        self.source = gogoanime.GoGoAnime()

    @commands.command(brief='Set the anime source for retrieving new anime')
    async def setAnimeSource(self, ctx, source: str):
        if source.lower() == "gogoanime":
            self.source = gogoanime.GoGoAnime()
        elif source.lower() == "9anime":
            self.source = _9anime._9Anime()
        else:
            await ctx.send('Unknown or unsupported anime source.')
            return
        self.list.clear()
        self.fillCache()
        await ctx.send(f'Successfully set the anime source to {source}.')

    @tasks.loop(minutes=5)
    async def checkNewLoop(self):
        await self.checkNew()
