
import discord
import jikanpy
from discord.ext import tasks, commands
from jikanpy import Jikan


class UserCog(commands.Cog):
    """
    UserCog: handles all the user-related logic.
    """

    def __init__(self, bot):
        """
        Constructor: initialize the cog.

        :param bot: The Discord bot.
        """
        self.bot = bot
        self.discordUser = None
        self.malUser = None
        self.channel = None
        self.jikan = Jikan()

    @commands.command(brief='Ping the bot')
    async def ping(self, ctx):
        """
        Ping the bot.

        :param ctx: The context.
        """
        await ctx.send(f'Pong: {round(self.bot.latency*1000)}ms')

    def start(self):
        """
        Start the UserCog:
            - retrieves the user from the database, if possible
            - start the updateMalProfileLoop
        """
        user = self.bot.get_cog('DatabaseCog').getUser()
        if user:
            try:
                self.malUser = self._getMALProfile(user['mal'])
            except jikanpy.exceptions.APIException:
                pass
            self.discordUser = self._getMember(user['discord'])
            self.channel = self._getChannel(user['channel'])

        self.updateMalProfileLoop.start()

    def _getMALProfile(self, username):
        """
        Get the MyAnimeList user object, given the username.

        :param username: The username of the MAL account.
        :return: The MAL user.
        """
        return self.jikan.user(username=username)

    def _updateMALProfile(self, profile):
        """
        Update the internal MAL user, i.e. updating the watching/reading list.

        :param profile: The username of the MAL account.
        """
        self.bot.get_cog('AnimeCog').list.clear()
        watching = self.jikan.user(username=profile, request='animelist', argument='watching')['anime']
        ptw = self.jikan.user(username=profile, request='animelist', argument='ptw')['anime']
        for anime in watching + ptw:
            anime['title_english'] = self.jikan.anime(anime['mal_id'])['title_english']
            self.bot.get_cog('AnimeCog').list.append(anime)
        self.bot.get_cog('MangaCog').list.clear()
        reading = self.jikan.user(username=profile, request='mangalist', argument='reading')['manga']
        ptr = self.jikan.user(username=profile, request='mangalist', argument='ptr')['manga']
        for manga in reading + ptr:
            manga['title_english'] = self.jikan.manga(manga['mal_id'])['title_english']
            self.bot.get_cog('MangaCog').list.append(manga)

    def _getMember(self, user):
        """
        Get the Discord member object, give its name and tag.

        :param user: The user (name + tag).
        :return: The member object, if none can be found, return None.
        """
        for member in self.bot.get_all_members():
            if str(member) == user:
                return member
        return None

    def _getChannel(self, channelName):
        """
        Get the Discord channel object, give the name of the channel.

        :param channelName: The name of the channel.
        :return: The channel object, if none can be found, return None.
        """
        for channel in self.bot.get_all_channels():
            if str(channel) == channelName:
                return channel
        return None

    @commands.command(brief='Set your MAL profile')
    async def setProfile(self, ctx, profile: str):
        """
        Set the internal MAL account, as well as the discord account and bot channel.

        :param ctx: The context.
        :param profile: Name of the MAL account.
        """
        try:
            self.malUser = self._getMALProfile(profile)
        except jikanpy.exceptions.APIException:
            await ctx.send(f'Unable to find user {profile}, make sure the profile is public.')
        await ctx.send('Successfully set profile, you\'ll now receive notifications for new anime episodes and manga chapters!')

        self.discordUser = ctx.author
        self.channel = ctx.channel

        # Store data in database
        self.bot.get_cog('DatabaseCog').addUser(profile, str(self.discordUser), str(ctx.channel))

        self._updateMALProfile(profile)

    @commands.command(brief='Get a brief overview of your MAL profile')
    async def getProfile(self, ctx):
        """
        Get the MAL profile in form of an embed

        :param ctx: The context.
        """
        if self.malUser:
            embed = discord.Embed(title=self.malUser['username'], color=discord.Color.green())
            embed.add_field(name="Watching/Plan-to-Watch", value=str(len(self.bot.get_cog('AnimeCog').list)))
            embed.add_field(name="Reading/Plan-to-Read", value=str(len(self.bot.get_cog('MangaCog').list)))
            embed.add_field(name="Link", value=self.malUser['url'])
            embed.set_thumbnail(url=self.malUser['image_url'])
            await ctx.send(embed=embed)
        else:
            await ctx.send("Profile is not set, please use `!setProfile <USERNAME>` first.")

    @commands.command(brief='Set the bot channel (where it will ping you)')
    async def setChannel(self, ctx, channel: discord.TextChannel):
        """
        Set the bot channel.

        :param ctx: The context.
        :param channel: Name of the bot channel.
        """
        self.channel = channel
        self.bot.get_cog('DatabaseCog').addUser(self.malUser['username'], str(self.discordUser), str(ctx.channel))
        await ctx.send(f'Successfully set bot channel to {channel.mention}.')

    @setChannel.error
    async def setChannelError(self, ctx, error):
        """
        Error Handler for setChannel.

        :param ctx: The context.
        :param error: The error raised.
        """
        await ctx.send(error.args[0])

    @tasks.loop(minutes=30)
    async def updateMalProfileLoop(self):
        """
        Loop that periodically updates the MAL account, i.e. update watching/reading list.
        """
        if self.malUser:
            await self._updateMALProfile(self.malUser['username'])
