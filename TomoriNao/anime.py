
import discord
import jikanpy
import requests
from discord.ext import tasks, commands
from jikanpy import Jikan
from lxml import html, etree


# we can use this cache to check whether an anime was just released
class CachedAnimes(list):

    def append(self, item):
        super(CachedAnimes, self).append(item)
        if len(self) > 8:
            self.pop(0)


class Anime(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.user = None
        self.watching = []
        self.channel = None
        self.cachedAnimes = CachedAnimes()
        self.jikan = Jikan()

    @commands.command()
    async def setProfile(self, ctx, profile: str):
        try:
            user = self.jikan.user(username=profile)
            self.user = user
            self.watching = self.jikan.user(username=profile, request='animelist', argument='watching')['anime']
            self.channel = ctx.channel
            self.checkNewAnime.start()
            await ctx.send('Successfully set profile, you\'ll now receive notifications for new anime episodes and manga chapters!')

        except jikanpy.exceptions.APIException:
            await ctx.send(f'Unable to find user {profile}, make sure the profile is public.')

    @commands.command()
    async def setChannel(self, ctx, channel: discord.TextChannel):
        self.channel = channel
        await ctx.send(f'Successfully set bot channel to {channel.mention}.')

    @setChannel.error
    async def setChannelError(self, ctx, error):
        await ctx.send(error.args[0])

    def getAnime(self):
        with requests.Session() as session:
            response = session.get('https://www1.9anime.nl/home')
            if response.status_code == 200:
                tree = html.fromstring(response.text)
                # Get all the recent anime's
                return tree.xpath("//div[contains(concat(' ', normalize-space(@class), ' '), ' content ') and not(contains(concat(' ', @class, ' '), ' hidden '))]/*[1]/*[1]/*")
        return None

    def cacheAnime(self):
        animes = self.getAnime()
        if animes:
            animes.reverse()
            for anime in animes:
                # Get the title
                query = anime.xpath("*[1]/a[contains(concat(' ', normalize-space(@class), ' '), ' name ')]/@data-jtitle")
                title = query[0] if len(query) > 0 else None
                if title:
                    self.cachedAnimes.append(title)

    async def sendPing(self, title, count, link, image):
        embed = discord.Embed(title=title, description=count, color=0xeee657)
        embed.add_field(name="Link", value=f"[{link}]({link})")
        embed.set_thumbnail(url=image)
        await self.channel.send(embed=embed)

    @tasks.loop(minutes=1)
    async def checkNewAnime(self):
        animes = self.getAnime()
        if animes:
            for anime in animes:
                # Get the title
                query = anime.xpath("*[1]/a[contains(concat(' ', normalize-space(@class), ' '), ' name ')]/@data-jtitle")
                title = query[0] if len(query) > 0 else None
                if title:
                    # Check if anime is in currently watching list
                    for watching in self.watching:
                        if title == watching['title'] and title not in self.cachedAnimes:
                            self.cachedAnimes.append(title)
                            ep = anime.xpath("//div[contains(concat(' ', normalize-space(@class), ' '), ' ep ')]")[0]
                            link = anime.xpath("*[1]/a[contains(concat(' ', normalize-space(@class), ' '), ' name ')]/@href")[0]
                            await self.sendPing(title, ep.text_content(), link, watching['image_url'])
        else:
            print(f'Failed retrieving data from 9anime')
