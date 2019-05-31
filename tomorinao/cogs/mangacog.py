
import discord
from discord.ext import tasks, commands

from tomorinao.cache import Cache
from tomorinao.cogs.manga.mangarock import MangaRock


class MangaCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.reading = []
        self.cachedMangas = Cache()     # we can use this cache to check whether a chapter was just released

        # Replace this with your own 'Manga API' if you want to use a different manga source
        self.manga = MangaRock()

    def fillCache(self):
        mangas = self.manga.getRecentManga()
        mangas.reverse()    # make sure the most recent ones are added last to the cache
        for manga in mangas:
            self.cachedMangas.append(manga.title)

    async def sendPing(self, title, count, link, image):
        embed = discord.Embed(title=title, description=count, color=discord.Color.green())
        embed.add_field(name="Link", value=f"[{link}]({link})")
        embed.set_thumbnail(url=image)
        await self.bot.get_cog('UserCog').channel.send(embed=embed)

    async def checkNewManga(self):
        mangas = self.manga.getRecentManga()
        for manga in mangas:
            if manga.title not in self.cachedMangas:
                self.cachedMangas.append(manga.title)
                # Check if manga is in currently reading list
                for reading in self.reading:
                    if manga.title == reading['title'] or manga.title == reading['title_english']:
                        await self.sendPing(manga.title, manga.ep, manga.link, reading['image_url'])

    @tasks.loop(minutes=1)
    async def checkNewMangaLoop(self):
        await self.checkNewManga()
