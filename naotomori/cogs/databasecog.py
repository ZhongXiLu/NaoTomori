
import os
import psycopg2
from psycopg2.extras import DictCursor
from discord.ext import commands


class DatabaseCog(commands.Cog):
    """
    DatabaseCog: handles all the database requests.
    """

    def __init__(self, bot):
        """
        Constructor: initialize the cog.

        :param bot: The Discord bot.
        """
        self.bot = bot
        try:
            self.conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
            self.cursor = self.conn.cursor(cursor_factory=DictCursor)
        except:
            raise RuntimeError("Failed connecting to Postgresql")

    def __del__(self):
        """
        Destructor: close the database connections.
        """
        self.cursor.close()
        self.conn.close()

    def start(self):
        """
        Start the DatabaseCog: creates the table if it didn't exist already.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS USERS (
                mal VARCHAR(32),
                discord VARCHAR(32),
                channel VARCHAR(100)
            );
        """)
        self.conn.commit()

    @commands.command(brief='Recreate the database (tables)')
    async def recreateDB(self, ctx):
        """
        Recreate the database, i.e. the 'USERS' table.
        :param ctx: The context.
        """
        self.cursor.execute("""
            DROP TABLE USERS;
        """)
        self.conn.commit()
        await ctx.send('Successfully recreated database.')
        self.start()

    @commands.command(brief='Get the database (the current user)')
    async def getDB(self, ctx):
        """
        Get the row of the 'USERS' table (should only be one atm), i.e. the current user.
        :param ctx: The context.
        """
        await ctx.send(f'`{self.getUser()}`')

    def addUser(self, mal, discord, channel):
        """
        Add a new user to the database, it either updates the existing one or it will create a new entry.

        :param mal: The MAL username.
        :param discord: The Discord username (name + tag).
        :param channel: The bot channel name.
        """

        # We're only storing one user, so truncate table to be sure that we only have on row in the table
        self.cursor.execute("""
            TRUNCATE USERS;
        """)
        self.conn.commit()

        self.cursor.execute("""
            INSERT INTO USERS (mal, discord, channel) VALUES (%s, %s, %s)
        """, (mal, discord, channel))
        self.conn.commit()

    def getUser(self):
        """
        Get the current user stored in the database.

        :return: Dictionary of the current user, if none exists, return None.
        """
        self.cursor.execute("""
            SELECT * FROM USERS LIMIT 1;
        """)
        self.conn.commit()
        return self.cursor.fetchone()
