
import os
import psycopg2
from psycopg2.extras import DictCursor
from discord.ext import commands


class DatabaseCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        try:
            self.conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
            self.cursor = self.conn.cursor(cursor_factory=DictCursor)
        except:
            raise RuntimeError("Failed connecting to Postgresql")

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def start(self):
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
        self.cursor.execute("""
            DROP TABLE USERS;
        """)
        self.conn.commit()
        await ctx.send('Successfully recreated database.')
        self.start()

    @commands.command(brief='Get the database (the current user)')
    async def getDB(self, ctx):
        await ctx.send(f'`{self.getUser()}`')

    def addUser(self, mal, discord, channel):

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
        self.cursor.execute("""
            SELECT * FROM USERS LIMIT 1;
        """)
        self.conn.commit()
        return self.cursor.fetchone()
