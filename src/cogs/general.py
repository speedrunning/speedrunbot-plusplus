from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="source")
    async def source(self, ctx):
        SRC = "https://www.github.com/Mango0x45/speedrunbot++"
        await ctx.send(SRC)

    @commands.command(name="ping")
    async def ping(self, ctx):
        LATENCY = round(self.bot.latency * 1000)
        await ctx.send(f"Pong! {LATENCY}ms")

    @commands.command(name="invite")
    async def invite(self, ctx):
        INV = "https://discord.com/oauth2/authorize?client_id=812751357119037460&scope=bot"
        await ctx.send(INV)


def setup(bot):
    bot.add_cog(General(bot))
