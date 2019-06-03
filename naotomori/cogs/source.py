
import discord
from discord.ext import tasks, commands

from naotomori.cache import Cache


class SourceCog(commands.Cog):
    """Abstract class for the AnimeCog and MangaCog"""

    def __init__(self, bot):
        self.bot = bot
        self.list = []  # currently watching/reading list
        self.cache = Cache(32)
        self.source = None

    def start(self):
        self.fillCache()
        self.checkNewLoop.start()

    def fillCache(self):
        items = self.source.getRecent()
        items.reverse()    # make sure the most recent ones are added last to the cache
        for item in items:
            self.cache.append(item.title)

    async def sendPing(self, title, count, link, image):
        embed = discord.Embed(title=title, description=count, color=discord.Color.green())
        embed.add_field(name="Link", value=f"[{link}]({link})")
        embed.set_thumbnail(url=image)
        await self.bot.get_cog('UserCog').channel.send(self.bot.get_cog('UserCog').discordUser.mention, embed=embed)

    async def checkNew(self):
        items = self.source.getRecent()
        items.reverse()
        if items:
            for item in items:
                if item.title not in self.cache:
                    print(f'{str(self.source)}: {item.title}')
                    self.cache.append(item.title)
                    for itemList in self.list:
                        if item.title == itemList['title'] or item.title == itemList['title_english']:
                            await self.sendPing(item.title, item.ep, item.link, itemList['image_url'])
        else:
            print(f'Failed retrieving from {str(self.source)}')

    @tasks.loop(minutes=5)
    async def checkNewLoop(self):
        pass
