
import discord
from discord.ext import tasks, commands

from tomorinao.cache import Cache
from tomorinao.cogs.anime import _9anime, gogoanime


class AnimeCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.watching = []
        self.cachedAnimes = Cache()     # we can use this cache to check whether an anime was just released

        # Replace this with your own 'Anime API' if you want to use a different anime source
        # self.anime = _9anime._9Anime()
        self.anime = gogoanime.GoGoAnime()

    def start(self):
        self.fillCache()
        self.checkNewAnimeLoop.start()

    @commands.command(brief='Set the anime source for retrieving new anime')
    async def setAnimeSource(self, ctx, source: str):
        if source.lower() == "gogoanime":
            self.anime = gogoanime.GoGoAnime()
        elif source.lower() == "9anime":
            self.anime = _9anime._9Anime()
        else:
            await ctx.send('Unknown or unsupported anime source.')
            return
        self.cachedAnimes.clear()
        self.fillCache()
        await ctx.send(f'Successfully set the anime source to {source}.')

    def fillCache(self):
        animes = self.anime.getRecentAnime()
        animes.reverse()    # make sure the most recent ones are added last to the cache
        for anime in animes:
            self.cachedAnimes.append(anime.title)

    async def sendPing(self, title, count, link, image):
        embed = discord.Embed(title=title, description=count, color=discord.Color.green())
        embed.add_field(name="Link", value=f"[{link}]({link})")
        embed.set_thumbnail(url=image)
        await self.bot.get_cog('UserCog').channel.send(embed=embed)

    async def checkNewAnime(self):
        animes = self.anime.getRecentAnime()
        if animes:
            for anime in animes:
                if anime.title not in self.cachedAnimes:
                    print(f'New anime: {anime.title}')
                    self.cachedAnimes.append(anime.title)
                    # Check if anime is in currently watching list
                    for watching in self.watching:
                        if anime.title == watching['title'] or anime.title == watching['title_english']:
                            await self.sendPing(anime.title, anime.ep, anime.link, watching['image_url'])
        else:
            print('Failed retrieving new anime')

    @tasks.loop(minutes=5)
    async def checkNewAnimeLoop(self):
        await self.checkNewAnime()
