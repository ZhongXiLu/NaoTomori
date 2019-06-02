
import discord
import jikanpy
from discord.ext import tasks, commands
from jikanpy import Jikan


class UserCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.discordUser = None
        self.malUser = None
        self.channel = None
        self.jikan = Jikan()

        self.updateMalProfileLoop.start()

    @commands.command(brief='Ping the bot')
    async def ping(self, ctx):
        await ctx.send(f'Pong: {round(self.bot.latency*1000)}ms')

    def _getMALProfile(self, username):
        return self.jikan.user(username=username)

    def _updateMALProfile(self, profile):
        self.bot.get_cog('AnimeCog').list.clear()
        for anime in self.jikan.user(username=profile, request='animelist', argument='watching')['anime']:
            anime['title_english'] = self.jikan.anime(anime['mal_id'])['title_english']
            self.bot.get_cog('AnimeCog').list.append(anime)
        self.bot.get_cog('MangaCog').list.clear()
        for manga in self.jikan.user(username=profile, request='mangalist', argument='reading')['manga']:
            manga['title_english'] = self.jikan.manga(manga['mal_id'])['title_english']
            self.bot.get_cog('MangaCog').list.append(manga)

    @commands.command(brief='Set your MAL profile')
    async def setProfile(self, ctx, profile: str):
        try:
            self.discordUser = ctx.author
            user = self._getMALProfile(profile)
            self._updateMALProfile(profile)
            self.malUser = user
            self.channel = ctx.channel
            await ctx.send('Successfully set profile, you\'ll now receive notifications for new anime episodes and manga chapters!')

        except jikanpy.exceptions.APIException:
            await ctx.send(f'Unable to find user {profile}, make sure the profile is public.')

    @commands.command(brief='Get a brief overview of your MAL profile')
    async def getProfile(self, ctx):
        if self.malUser:
            embed = discord.Embed(title=self.malUser['username'], color=discord.Color.green())
            embed.add_field(name="Watching", value=str(len(self.bot.get_cog('AnimeCog').list)))
            embed.add_field(name="Reading", value=str(len(self.bot.get_cog('MangaCog').list)))
            embed.add_field(name="Link", value=self.malUser['url'])
            embed.set_thumbnail(url=self.malUser['image_url'])
            await ctx.send(embed=embed)
        else:
            await ctx.send("Profile is not set, please use `!setProfile <USERNAME>` first.")

    @commands.command(brief='Set the bot channel (where it will ping you)')
    async def setChannel(self, ctx, channel: discord.TextChannel):
        self.channel = channel
        await ctx.send(f'Successfully set bot channel to {channel.mention}.')

    @setChannel.error
    async def setChannelError(self, ctx, error):
        await ctx.send(error.args[0])

    @tasks.loop(minutes=30)
    async def updateMalProfileLoop(self):
        if self.malUser:
            await self._updateMALProfile(self.malUser['username'])
