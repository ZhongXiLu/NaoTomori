
from discord.ext import tasks, commands

from naotomori.cogs.manga.mangarock import MangaRock
from naotomori.cogs.sourcecog import SourceCog


class MangaCog(SourceCog):

    def __init__(self, bot):
        super().__init__(bot)

        # Replace this with your own 'Manga API' if you want to use a different manga source
        self.source = MangaRock()

    @commands.command(brief='Set the manga source for retrieving new manga')
    async def setMangaSource(self, ctx, source: str):
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
        await self.checkNew()
