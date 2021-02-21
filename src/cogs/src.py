import discord
from discord.ext import commands

PREFIX = "./srcom/bin"


class Src(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="wrs")
    async def wrs(self, ctx, PLAYER=None):
        if not PLAYER:
            await ctx.send("Usage: `!wrs [PLAYER NAME]`")
            return

        COUNTS = self.bot.run_prog(f"{PREFIX}/wrs", PLAYER).split(" ")
        embed = discord.Embed(
            title=f"World Record Count: {PLAYER}",
            description=f"**Full Game**: {COUNTS[0]}\n**Individual Level**: {COUNTS[1]}\n**Total**: {COUNTS[2]}",
        )
        await ctx.send(embed=embed)

    @commands.command(name="runs")
    async def runs(self, ctx, PLAYER=None):
        if not PLAYER:
            await ctx.send("Usage: `!runs [PLAYER NAME]`")
            return

        COUNTS = self.bot.run_prog(f"{PREFIX}/runs.py", PLAYER).split(" ")
        embed = discord.Embed(
            title=f"Run Count: {PLAYER}",
            description=f"**Full Game**: {COUNTS[0]}\n**Individual Level**: {COUNTS[1]}\n**Total**: {COUNTS[2]}",
        )
        await ctx.send(embed=embed)

    @commands.command(name="games")
    async def games(self, ctx, PLAYER=None):
        if not PLAYER:
            await ctx.send("Usage: `!games [PLAYER NAME]`")
            return

        COUNT = self.bot.run_prog(f"{PREFIX}/games.py", PLAYER)
        embed = discord.Embed(
            title=f"Games Played: {PLAYER}",
            description=f"Games: {COUNT}",
        )
        await ctx.send(embed=embed)

    @commands.command(name="modcount")
    async def runs(self, ctx, PLAYER=None):
        if not PLAYER:
            await ctx.send("Usage: `!modcount [PLAYER NAME]`")
            return

        COUNTS = self.bot.run_prog(f"{PREFIX}/modcount.py", PLAYER).split(" ")
        embed = discord.Embed(
            title=f"Leaderboards Moderated: {PLAYER}",
            description=f"**Games**: {COUNTS[0]}\n**Series**: {COUNTS[1]}\n**Total**: {COUNTS[2]}",
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Src(bot))
