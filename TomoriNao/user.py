
import discord
import jikanpy
from discord.ext import commands
from jikanpy import Jikan


class User(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.user = None
        self.channel = None
        self.jikan = Jikan()

    @commands.command()
    async def setProfile(self, ctx, profile: str):
        try:
            user = self.jikan.user(username=profile)
            self.user = user
            self.channel = ctx.channel
            self.bot.get_cog('Anime').watching = self.jikan.user(username=profile, request='animelist', argument='watching')['anime']
            self.bot.get_cog('Anime').checkNewAnimeLoop.start()
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
