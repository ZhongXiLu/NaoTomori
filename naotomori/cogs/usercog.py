
import discord
import jikanpy
from discord.ext import tasks, commands
from jikanpy import Jikan
from tinydb import TinyDB, Query


class UserCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.discordUser = None
        self.malUser = None
        self.channel = None
        self.jikan = Jikan()
        self.db = TinyDB('db.json')

    @commands.command(brief='Ping the bot')
    async def ping(self, ctx):
        await ctx.send(f'Pong: {round(self.bot.latency*1000)}ms')

    def start(self):
        query = Query()
        if self.db.search(query.discordUser.exists()):
            malUser = self.db.search(query.malUser.exists())[0]['malUser']
            discordUser = self.db.search(query.discordUser.exists())[0]['discordUser']
            channel = self.db.search(query.channel.exists())[0]['channel']

            try:
                self.malUser = self._getMALProfile(malUser)
            except jikanpy.exceptions.APIException:
                pass
            self.discordUser = self._getMember(discordUser)
            self.channel = self._getChannel(channel)

        self.updateMalProfileLoop.start()

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

    def _getMember(self, user):
        for member in self.bot.get_all_members():
            if str(member) == user:
                return member
        return None

    def _getChannel(self, channelName):
        for channel in self.bot.get_all_channels():
            if str(channel) == channelName:
                return channel
        return None

    @commands.command(brief='Set your MAL profile')
    async def setProfile(self, ctx, profile: str):
        try:
            self.malUser = self._getMALProfile(profile)
        except jikanpy.exceptions.APIException:
            await ctx.send(f'Unable to find user {profile}, make sure the profile is public.')
        await ctx.send('Successfully set profile, you\'ll now receive notifications for new anime episodes and manga chapters!')

        self.discordUser = ctx.author
        self.channel = ctx.channel

        # Store data in database
        query = Query()
        if not self.db.search(query.discordUser.exists()):
            # Data not in db yet
            self.db.insert({'malUser': profile})
            self.db.insert({'discordUser': str(self.discordUser)})
            self.db.insert({'channel': str(ctx.channel)})
        else:
            # Data already in db => update it
            self.db.update({'malUser': profile}, query.malUser.exists())
            self.db.update({'discordUser': str(self.discordUser)}, query.discordUser.exists())
            self.db.update({'channel': str(ctx.channel)}, query.channel.exists())

        self._updateMALProfile(profile)

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
