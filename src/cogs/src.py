import discord
from discord.ext import commands

PREFIX: str = "./srcom/bin"


class Src(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="wrs")
    async def wrs(self, ctx, PLAYER: str = None):
        if not PLAYER:
            await ctx.send("Usage: `!wrs [PLAYER NAME]`")
            return

        RET: str = self.bot.run_prog(f"{PREFIX}/wrs", PLAYER)
        embed = discord.Embed(
            title=f"World Record Count: {PLAYER}",
            description=RET,
        )
        await ctx.send(embed=embed)

    @commands.command(name="runs")
    async def runs(self, ctx, PLAYER: str = None):
        if not PLAYER:
            await ctx.send("Usage: `!runs [PLAYER NAME]`")
            return

        RET: str = self.bot.run_prog(f"{PREFIX}/runs", PLAYER)
        embed = discord.Embed(title=f"Run Count: {PLAYER}", description=RET)
        await ctx.send(embed=embed)

    @commands.command(name="games")
    async def games(self, ctx, PLAYER: str = None):
        if not PLAYER:
            await ctx.send("Usage: `!games [PLAYER NAME]`")
            return

        RET: str = self.bot.run_prog(f"{PREFIX}/games", PLAYER)
        embed = discord.Embed(
            title=f"Games Played: {PLAYER}",
            description=RET,
        )
        await ctx.send(embed=embed)

    @commands.command(name="modcount", aliases=["mc"])
    async def modcount(self, ctx, PLAYER: str = None):
        if not PLAYER:
            await ctx.send("Usage: `!modcount [PLAYER NAME]`")
            return

        RET: str = self.bot.run_prog(f"{PREFIX}/modcount", PLAYER)
        embed = discord.Embed(
            title=f"Leaderboards Moderated: {PLAYER}",
            description=RET,
        )
        await ctx.send(embed=embed)

    @commands.command(name="leaderboard", aliases=["lb"])
    async def leaderboard(self, ctx, GAME: str = None, CAT: str = None):
        if not GAME:
            await ctx.send("Usage: `!leaderboard [GAME] [CATEGORY (Optional)]`")
            return

        RET: str = self.bot.run_prog(
            f"{PREFIX}/leaderboard", f"{GAME} {CAT}"
        ).split("\n")
        embed = discord.Embed(
            title=f"Top 10: {RET[0]}",
            description="```" + "\n".join(RET[1:]) + "```",
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Src(bot))
