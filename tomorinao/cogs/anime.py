
import discord
import requests
from discord.ext import tasks, commands
from lxml import html

from tomorinao.cache import Cache


class Anime(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.watching = []
        self.cachedAnimes = Cache()     # we can use this cache to check whether an anime was just released

    def findAnimeElements(self, tree):
        return tree.xpath("//div[contains(concat(' ', normalize-space(@class), ' '), ' content ') and not(contains(concat(' ', @class, ' '), ' hidden '))]/*[1]/*[1]/*")

    def getRecentAnime(self):
        with requests.Session() as session:
            response = session.get('https://www1.9anime.nl/home')
            if response.status_code == 200:
                tree = html.fromstring(response.text)
                # Get all the recent anime's
                return self.findAnimeElements(tree)
        return None

    def fillCache(self):
        animes = self.getRecentAnime()
        if animes:
            animes.reverse()
            for anime in animes:
                # Get the title
                query = anime.xpath("*[1]/a[contains(concat(' ', normalize-space(@class), ' '), ' name ')]/@data-jtitle")
                title = query[0] if len(query) > 0 else None
                if title:
                    self.cachedAnimes.append(title)

    async def sendPing(self, title, count, link, image):
        embed = discord.Embed(title=title, description=count, color=discord.Color.green())
        embed.add_field(name="Link", value=f"[{link}]({link})")
        embed.set_thumbnail(url=image)
        await self.bot.get_cog('user').channel.send(embed=embed)

    async def checkNewAnime(self):
        animes = self.getRecentAnime()
        if animes:
            animes.reverse()
            for anime in animes:
                # Get the title
                query = anime.xpath(
                    "*[1]/a[contains(concat(' ', normalize-space(@class), ' '), ' name ')]/@data-jtitle")
                title = query[0] if len(query) > 0 else None
                if title:
                    if title not in self.cachedAnimes:
                        self.cachedAnimes.append(title)
                        # Check if anime is in currently watching list
                        for watching in self.watching:
                            if title == watching['title']:
                                ep = anime.xpath("//div[contains(concat(' ', normalize-space(@class), ' '), ' ep ')]")[0]
                                link = anime.xpath("*[1]/a[contains(concat(' ', normalize-space(@class), ' '), ' name ')]/@href")[0]
                                await self.sendPing(title, ep.text_content(), link, watching['image_url'])
        else:
            print(f'Failed retrieving data from 9anime')

    @tasks.loop(minutes=1)
    async def checkNewAnimeLoop(self):
        await self.checkNewAnime()
