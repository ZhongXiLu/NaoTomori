
import discord
import requests
import urllib
import shutil
from lxml import html, etree
from discord.ext import tasks, commands


class Anime(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.profile = ""
        self.channel = ""

    @commands.command()
    async def setProfile(self, ctx, profile: str):

        with requests.Session() as session:
            response = session.get(f'https://myanimelist.net/animelist/{profile}')
            if response.status_code == 200:
                self.profile = profile
                self.channel = ctx.channel
                self.checkNewAnime.restart()
                await ctx.send('Successfully set profile, you\'ll now receive notifications for new anime episodes and manga chapters!')

            else:
                await ctx.send(f'Unable to find user {profile}, make sure the profile is public.')

    @commands.command()
    async def setChannel(self, ctx, channel: discord.TextChannel):
        self.channel = channel
        await ctx.send(f'Successfully set bot channel to {channel.mention}.')

    @setChannel.error
    async def setChannelError(self, ctx, error):
        await ctx.send(error.args[0])

    @commands.command()
    async def test(self, ctx):
        embed = discord.Embed(title="New Anime episode", description="@everyone", color=0xeee657)
        embed.add_field(name="Link",
                        value="[https://www1.9anime.nl/watch/charlotte.l8n](https://www1.9anime.nl/watch/charlotte.l8n)")
        await ctx.send(embed=embed)

    @tasks.loop(seconds=10.0)
    async def checkNewAnime(self):
        channel = next(self.bot.get_all_channels())     # get default channel
        if channel is not None:
            pass
            # await channel.send("test")
