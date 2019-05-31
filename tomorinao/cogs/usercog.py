
import discord
import jikanpy
from discord.ext import commands
from jikanpy import Jikan


class UserCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.user = None
        self.channel = None
        self.jikan = Jikan()

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong: {round(self.bot.latency*1000)}ms')

    @commands.command()
    async def setProfile(self, ctx, profile: str):
        try:
            user = self.jikan.user(username=profile)
            self.user = user
            self.channel = ctx.channel
            self.bot.get_cog('AnimeCog').watching = self.jikan.user(username=profile, request='animelist', argument='watching')['anime']
            self.bot.get_cog('AnimeCog').checkNewAnimeLoop.start()
            await ctx.send('Successfully set profile, you\'ll now receive notifications for new anime episodes and manga chapters!')

        except jikanpy.exceptions.APIException:
            await ctx.send(f'Unable to find user {profile}, make sure the profile is public.')

    @commands.command()
    async def getProfile(self, ctx):
        if self.user:
            embed = discord.Embed(title=self.user['username'], color=discord.Color.green())
            embed.add_field(name="Watching", value=str(len(self.bot.get_cog('AnimeCog').watching)))
            embed.set_thumbnail(url=self.user['image_url'])
            await ctx.send(embed=embed)
        else:
            await ctx.send("Profile is not set, please use `!setProfile <USERNAME>` first.")

    @commands.command()
    async def setChannel(self, ctx, channel: discord.TextChannel):
        self.channel = channel
        await ctx.send(f'Successfully set bot channel to {channel.mention}.')

    @setChannel.error
    async def setChannelError(self, ctx, error):
        await ctx.send(error.args[0])
