from discord.ext import commands

class PingCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot                  # keep bot instance
    
    @commands.command()
    async def ping(self, ctx):          # -ping
        user_name = ctx.author.name
        await ctx.send("pong!")
        await ctx.send(f"Hello, {user_name}!")

async def setup(bot):
    await bot.add_cog(PingCommands(bot))
